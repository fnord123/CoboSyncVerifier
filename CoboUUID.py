#!/usr/bin/python3

# verify uuid on the Cobo Vault device

from bip_utils import Bip32, Bip32Utils, Bip39SeedGenerator

Cobo_PATH = "M/44'/1131373167'/0'"  # 1131373167 stand for Cobo
"""
    1131373167 stand for Cobo of int
    
    brand_name = 'Cobo'
    brand_name_bytes = brand_name.encode()
    brand_name_hex = brand_name_bytes.hex()
    brand_name_int = int(brand_name_hex, 16)
    print(brand_name_int) #1131373167

"""


def generate_uuid(mnemonic, passpharse=""):

    seed_bytes = Bip39SeedGenerator(mnemonic).Generate(passpharse)

    bip32_root = Bip32.FromSeed(seed_bytes)

    cobo_extend_key = (
        bip32_root.ChildKey(Bip32Utils.HardenIndex(44))
        .ChildKey(Bip32Utils.HardenIndex(1131373167))
        .ChildKey(Bip32Utils.HardenIndex(0))
    )
    public_key = cobo_extend_key.PublicKey().RawCompressed().ToHex()
    uuid = public_key[2:]
    return uuid


if __name__ == "__main__":
    # replace this to your mnemonic to be verified
    MNEMONIC = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    uuid = generate_uuid(MNEMONIC)
    print('UUID is', uuid)
