#!/usr/bin/python3

# Decode the values that a Cobo Vault device displays to the Cobo Vault app in order
# to verify that only xpub and other non-secure information is allowed to leak from
# a Cobo Vault device.

import argparse
import base64
import gzip

def verify_urheader(urHeader, indice):
  if urHeader != "UR:BYTES":
    raise Exception("workload %i doesn't begin with expected header" % indice)

def verify_sequence(piece, indice):
  sequence = list(map(int, piece.split("OF")))
  if len(sequence) != 2:
    raise Exception("workload %i sequence has unexpected number of values" % indice)
  index = sequence.pop(0)
  if index < 1:
    raise Exception("workload has an invalid sequence index %i" % index)
  total = sequence.pop(0)
  if index > total:
    raise Exception("workload has an index %i larger than total %i" % (index, total))
  return index


def fiveBitsToEight(fivebit_values):
  byte_values = []
  current_word = 0
  bits = 0

  for fivebits in fivebit_values:
    current_word = (current_word << 5) | fivebits
    bits += 5
    while bits > 8:
      bits -= 8
      byte = current_word >> bits & 0xFF
      byte_values.append(byte)
      current_word &= 0xFF
  return byte_values

def decode_bech32(bech32Payload):
  BECH32_CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
  if len(bech32Payload) < 6:
    raise Exception("Payload input too short")
  if any(map(str.isupper, bech32Payload)) and any(map(str.islower, bech32Payload)):
    raise Exception("Payload has illegal mixing of upper and lower case")
  if not bech32Payload.isalnum():
    raise Exception("Invalid character found in payload")
  fivebit_values = []
  for c in list(bech32Payload.lower()):
    fivebit_values += bytes([BECH32_CHARSET.index(c)])
  # Should verify checksum here but it isn't necessary for inspecting the payload
  # for leaking of secret key related info. Instead just remove it (last 6B)
  del fivebit_values[-6:]
  #print(fivebit_values[:20])
  decoded_bytes = fiveBitsToEight(fivebit_values)
  #print(decoded_bytes[:20])
  return decoded_bytes


parser = argparse.ArgumentParser(description='Decode a Cobo Vault sync message.')
parser.add_argument("--filename", type=str, default="sample_qr_codes.txt",
                    help="Name of the file containing the Cobo Vault sync data")
args = parser.parse_args()
with open(args.filename) as f:
    content = f.readlines()
# remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content] 
fragments = [None] * len(content)
digest = ""
for indice, workload in enumerate(content, start=1):
  pieces = workload.split('/')
  if len(pieces) != 4:
    raise Exception("Unexpected number of pieces in workload %i" % indice)
  verify_urheader(pieces.pop(0), indice)
  index = verify_sequence(pieces.pop(0), indice)
  if digest == "":
    digest = pieces.pop(0)
  elif digest != pieces.pop(0):
    raise Exception("invalid workload, digest changed")
  payload = pieces.pop(0)
  if fragments[index-1] != None:
    raise Exception("invalid workload, index %i already set" % index)
  fragments[index-1] = payload
bech32Payload = ''.join(map(str, fragments))
payload = decode_bech32(bech32Payload)
if (payload[0] != 0x59):
  raise Exception ("unexpected header")
dataLength = payload[1] * 256 + payload[2]
payload = payload[3:]
if dataLength != len(payload):
  raise Exception("unexpected length")
unzippedPayload = gzip.decompress(bytearray(payload))
#listOfLines = unzippedPayload.split(b'\n')
print(unzippedPayload.hex())
undecodedPayload = base64.b64decode(unzippedPayload.hex())
print(undecodedPayload)
