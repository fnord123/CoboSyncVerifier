#!/usr/bin/python3

# Python equivalent of what the Cobo Vault device does to generate the UUID that
# is shown to the Cobo App during pairing.

# Note that these are only available after pip3 install bip_utils. Doing so requires
# an Internet connection and the ability to run pip3, which is problematic on TAILS.
# See the README.md for an equivalent way to do all the following on TAILS.
from bip_utils import Bip32, Bip32Utils, Bip39SeedGenerator

# 1131373167 is the word 'Cobo' encoded as shown below
Cobo_PATH = "M/44'/1131373167'/0'"
"""
    1131373167 stand for the bytes of the word 'Cobo', represented using an int
    
    brand_name = 'Cobo'
    brand_name_bytes = brand_name.encode()
    brand_name_hex = brand_name_bytes.hex()
    brand_name_int = int(brand_name_hex, 16)
    print(brand_name_int) #1131373167

"""

# This is the python equivalent of the code that actually runs on a Cobo Vault
# to generate the UUID value that is used in pairing a vault with the Cobo Vault App
# on a phone.
def generate_uuid(mnemonic, passphrase=""):
    # At this point the Cobo Vault hardware is directly using the (secret)
    # BIP39 mnemonic, converting it to a BIP39 seed value.  If one is using a
    # Shamir (SLIP39) mnemonic a different path is taken to generate these
    # seed bytes.
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate(passphrase)

    # From this point onwards the code is identical whether a BIP39 or SLIP39
    # mnemonic.  The following extracts the BIP32 Root Key. This is still secret
    # data that we don't want leaking from the Cobo Vault hardware.
    bip32_root = Bip32.FromSeed(seed_bytes)

    # Given the BIP32 root key, derive a BIP32 extended (public/private) keypair,
    # using Cobo's BIP32 derivation path.  Note that this path is only used for
    # generating the 'UUID' used by the Cobo Vault (and app).  For coin-specific
    # (e.g. Bitcoin etc.) keys the Cobo Vault hardware and App use more typical
    # hardened paths that are commonly used -  E.g. m/49'/0'/0' for bitcoin,
    # m/44'/60'/0' for Ethereum, etc. Still secret data here!
    cobo_extend_key = (
        bip32_root.ChildKey(Bip32Utils.HardenIndex(44))
        .ChildKey(Bip32Utils.HardenIndex(1131373167))
        .ChildKey(Bip32Utils.HardenIndex(0))
    )

    # Up until this point the Cobo Vault hardware has been dealing with secret
    # information that should never be leaked outside the device, as doing so
    # would allow stealing of one's keys and thus cryptocurrency.  The next step
    # discards the private key information and extracts the public key only.  The
    # public key can be used to find all transactions associated with a wallet, but
    # it *cannot* be used to spend (or steal) cryptocurrency.
    public_key = cobo_extend_key.PublicKey().RawCompressed().ToHex()

    # After discarding the private (secret) key, compress the public key and remove
    # a couple bytes to produce the 'uuid'.
    uuid = public_key[2:]
    return uuid


if __name__ == "__main__":
    # Example mnemonic.  If one wants to try their own BIP39 mnemonic then do so
    # here, *HOWEVER* only do so on a secure compute environment - e.g. a laptop
    # with no HD/SSD, running TAILS OS off a USB key, on airplane mode.
    # If you want to try a Shamir mnemonic, just override the seed_bytes value
    # in the generate_uuid function with the seed bytes from the Shamir mnemonic.
    BIP39_MNEMONIC = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    uuid = generate_uuid(BIP39_MNEMONIC)
    print('UUID is', uuid)
