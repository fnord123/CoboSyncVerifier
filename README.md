# CoboSyncVerifier
The Cobo Vault looks like one of the most secure hardware wallets available for Bitcoin and other cryptocurrencies.  By avoiding having any sort of electronic links (e.g. USB, as in the case of Trezor, or Bluetooth + USB, as in Ledger Nano X), it significantly reduces the attack surface wherein a malicious actor could get access to someone's private keys and thus steal their crypto currencies.

Cobo Vault does has one feature that needs examination.  The Cobo Vault supports a watch-only wallet in the form of the Cobo Vault App for iOS and Android, which allows users to monitor their cryptocurrency transactions and balances.  To use the app, the user must do a one-time pairing of the Vault hardware device to the app.  This is done by a series of QR codes that the vault displays to the app.

This display of QR codes is an area that needs examination.  It is *possible* that these QR codes could carry the user's secret keys and expose it to the Cobo Vault App, which in turn could relay it to a malicious actor.  That malicious actor could then choose to sweep all of one's bitcoins or other cryptocurrency.  Note that for this to be an actual attack, it would require the authors of both the Cobo Vault firmware and the Cobo App be in collusion.  While unlikely, this is possible as they both work for the same entity - Cobo.

While Cobo has not done anything to indicate they are a bad actor,  it is still better if a crypto currency user verifies for themselves that nothing suspicious is going on.  Specifically, before one loads any significant amount of currency onto a Cobo Vault, one should first independently parse the QR codes used in pairing it to the Cobo App to make sure the content doesn't contain any secret information.

The code in this repository can be used for this purpose.  It decodes the Cobo Vault's QR code content in an easily understandable fashion and shows to the user exactly what the Vault is sending to the app, allowing the user to verify that no secrets are being transmitted.

To run this the following pre-requisites must be fulfilled:
1) Google Protobuf compiler.  On Ubuntu this can be installed by doing:<br>
`sudo apt install protobuf-compiler`
2) Google Python API client for protobufs. Assuming python3, this can be installed by doing:<br>
`pip3 install --upgrade google-api-python-client`
3) pip install bip_utils for verify the uuid 
`pip3 install bip-utils==1.7.0`
4) Run (and install if necessary) `make` to build the python modules needed for Google proto3 support.

Once the above pre-requisites are met, the following sequence can be used to verify the safety of the contents of the QR Codes the Cobo Vault shows to the Cobo App during pairing.  If one wants to ensure the security of their cryptocurrency, do **not** load any currency onto the Cobo Vault until the following sequence has been successfully completed.
1) Turn on the Cobo Vault, click on the menu hamburger in the top-left ocrner, and select *Watch-only Wallet*
2) Click on *Cobo Vault App*.  If it is already selected and the *Confirm* button is greyed out, you will need to choose another entry (e.g. *Polkadot.js*), then confirm, then click the *<* arrow to go back and re-select *Cobo Vault App*, then click the (now blue) *Confirm* button.
3) Select any cryptocurrencies desired, then click the check mark at the top-right corner of the screen.
4) On the next screen, click the *Display QR Code* blue button at the bottom.
5) The Cobo Vault will begin rapidly displaying a set of QR codes. Press the *Difficulty scanning? Tap the QR code to adjust.* button.
6) Press the pause button on the resulting screen and use the slider to maximize the size of the QR code, then scan the first image with the Cobo Vault app and with a QR Code Scanner of your choice.  I used 'Codex - QR Code for Windows 10' as a free app from the Microsoft store to do this, but any app can be used that allows saving the resultant text to a file.
7) Scan the first QR code with the Cobo App, it will tell you something like "1 of 3 done". Go ahead and click the right arrow on the vault to display the next QR code, then repeat the process from step 6.  Do this until the Cobo App says it is done, scanning each QR code with both the Cobo App and with your own selected QR code scanner.  
8) Put down the Cobo Vault device and leave the QR code subscreen.  At this point one should never have to display these QR codes again unless pairing has to be done again e.g. with a new phone.
9) Save the text of the Cobo Vault QRcodes (captured using your QR code scanner) into a file accessible by the code in this repository.  The resulting file should look like the [example file in this repo](sample_qr_codes.txt).
10) Run the verifier code against the file, e.g.<br>`./coboVerify.py --file sample_qr_codes.txt`
11) The verifier will decode the QRCode text files and show exactly what they contain. It should look something like this:<br>
```
*************************************************************
Following is entire message sent via QRCode from vault to app
*************************************************************
version: 1
description: "cobo vault qrcode"
data {
  type: TYPE_SYNC
  uuid: "641d6af6cb503f33ab63829cc77b39dbb0618b963ca9b984ad427e65de9c6267"
  sync {
    coins {
      coinCode: "BTC"
      active: true
      accounts {
        hdPath: "M/49\'/0\'/0\'"
        xPub: "xpub6C6nQwHaWbSrzs5tZ1q7m5R9cPK9eYpNMFesiXsYrgc1P8bvLLAet9JfHjYXKjToD8cBRswJXXbbFpXgwsswVPAZzKMa1jUp2kVkGVUaJa7"
        addressLength: 1
      }
    }
...
    coins {
      coinCode: "CFX"
      accounts {
        hdPath: "M/44\'/503\'/0\'"
        xPub: "xpub6BtifpKfg5jVAoq27YcCUxExKSsbDMnGgFBBHZVBSL5VRYG4JLXjq9KyJc1Tb8mLnhpwgEDsMFdMtWD5M3b16wiJcXCD51ooomndAWQmYqs"
        addressLength: 1
      }
    }
  }
}
coldVersion: 20400
deviceType: "Cobo Vault Pro"
*************************************************************
At this point one should verify each of the XPUBs shown above, and
the UUID shown below (also at the top of the above output). See the
README.md for how to do that.
UUID is 641d6af6cb503f33ab63829cc77b39dbb0618b963ca9b984ad427e65de9c6267
```

As one can see, most of the payload is understandable and does not appear to contain any secrets.  However, to be maximally secure, the user should go through each of the xPub entries listed above and independently derive them. 

**TODO:** Add instructions how to do that.

The UUID stands for the the unique identifier.  Cobo derives this value from the BIP32 Extended Public Key derived from the user's mnemonic.  The [CoboUUID.py](CoboUUID.py) file in this repository shows the steps Cobo uses to generate the UUID.

At this point, the user has a few choices:
- Accept the code as is. Trust that Cobo is on the up and up, and that I (the author of this website), who did the following steps, are honest actors.  In doing so you already are a step ahead of the typical Trezor or Ledger user because you have at least looked at how the device communicates to the outside world.  Unless you have an (expensive) USB scanner and/or Bluetooth scanner you can't do the same with those other devices.
- Verify all the xPubs shown are truly derived xPubs from the BIP32 Extended Public Key.  This is useful to do because it ensures they truly are derived xPUBs and not a backdoor way of leaking private keys.  Instructions coming later for how to do this.
- Verify that the 'UUID' shown by your device was generated using the same algorithm that [CoboUUID.py](CoboUUID.py) shows.  Note that this algorithm makes use of secret information, so it should only be done on a secure compute environment.  Specifically, a laptop with no HD or SSD, running TAILS OS booted off a USB key.  Temporarily connect to the Internet long enough to install the prerequisites listed above, then switch to airplane mode and use CoboUUID.py to verify the UUID.

To audit the source code that Cobo Vault uses, refer to the [Cobo Github repository](https://github.com/CoboVault/cobo-vault-cold/blob/master/app/src/main/java/com/cobo/cold/callables/GetUuidCallable.java#L30)
