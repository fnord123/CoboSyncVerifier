# CoboSyncVerifier
The Cobo Vault appears to be one of the most secure hardware wallets available for Bitcoin and other cryptocurrencies.  By avoiding having any sort of electronic links (e.g. USB, as in the case of Trezor, or Bluetooth + USB, as in Ledger), it significantly reduces the attack surface wherein a malicious actor could get access to someone's private keys and thus steal their crypto currencies.

Cobo Vault does however have one potentially risky attack surface that needs examination.  The Cobo Vault supports a watch-only wallet in the form of the Cobo Vault App for iOS and Android, which allows users to monitor their cryptocurrency transactions and balances.  To use the app, the user must do a one-time pairing of the Vault hardware device to the app.  This is done by a series of QR codes that the vault displays to the app.

This display of QR codes is where the potential attack surface resides.  It is *possible* that these QR codes could carry the user's secret and expose it to the Cobo Vault App, which in turn could relay it to a malicious actor.  That actor could then sweep all of one's bitcoins if the value was high enough.  Note that for this attack vector to exist, it would require the authors of both the Cobo Vault firmware and the Cobo App be in collusion.  While unlikely, this is possible as they both work for the same entity - Cobo.

While Cobo has not done anything to indicate they are a bad actor,  it is still better if a crypto currency user verifies for themselves that nothing suspicious is going on.  Specifically, before one loads any significant amount of currency onto a Cobo Vault, one should first independently parse the QR codes used in pairing it to the Cobo App to make sure the content doesn't contain any secret information.

The code in this repository can be used for this purpose.  It decodes the Cobo Vault's QR code content in an easily understandable fashion and shows to the user exactly what the Vault is sending to the app, allowing the user to verify that no secrets are being transmitted.

To run this the following pre-requisites must be fulfilled.

1) Google Protobuf compiler.  On Ubuntu this can be installed by doing:<br>
`sudo apt install protobuf-compiler`

2) Google Python API client for protobufs. Assuming python3, this can be installed by doing:<br>
`pip3 install --upgrade google-api-python-client`

3) Run (and install if necessary) `make` to build the python modules needed for Google proto3 support.

Once the above pre-requisites are met, the following sequence can be used to verify the safety of the contents of the QR Codes the Cobo Vault shows to the Cobo App during pairing.
1) Turn on the Cobo Vault, click on the menu hamburger in the top-left ocrner, and select *Watch-only Wallet*
2) Click on *Cobo Vault App*.  If it is already selected and the *Confirm* button is greyed out, you will need to choose another entry (e.g. *Polkadot.js*), then confirm, then click the *<* arrow to go back and re-select *Cobo Vault App*, then click the (now blue) *Confirm* button.
3) Select any cryptocurrencies desired, then click the check mark at the top-right corner of the screen.
4) On the next screen, click the *Display QR Code* blue button at the bottom.
5) The Cobo Vault will begin rapidly displaying a set of QR codes. Press the *Difficulty scanning? Tap the QR code to adjust.* button.
6) Press the pause button on the resulting screen and use the slider to maximize the size of the QR code, then scan the first image with the Cobo Vault app and with a QR Code Scanner of your choice.  I used 'Codex - QR Code for Windows 10' as a free app from the Microsoft store to do this, but any app can be used that allows saving the resultant text to a file. 
7) After scanning the first QR code with the Cobo App, it will tell you something like "1 of 3 done". Go ahead and click the right arrow on the vault to display the next QR code, then repeat the process from step 6.  Do this until the Cobo App says it is done, scanning each QR code with both the Cobo App and with your own selected QR code scanner.
8) Save the text of the Cobo Vault QRcodes (captured using your QR code scanner) into a file accessible by the code in this repository.  The resulting file should look like the [example file in this repo](sample_qr_codes.txt).
9) Run the verifier code against the file, e.g.<br>`./coboVerify.py --file sample_qr_codes.txt`
10) The verifier will decode the files and show exactly what they contain. It should look something like this:<br>
```
*************************************************************
Following is entire message sent via QRCode from vault to app
*************************************************************
version: 1
description: "cobo vault qrcode"
data {
  type: TYPE_SYNC
  uuid: "a072a758ff78d50b27db92533dd0a3dcbfa92f2825b5a2d65d27e0659c8389ef"
  sync {
    coins {
      coinCode: "BTC"
      active: true
      accounts {
        hdPath: "M/49\'/0\'/0\'"
        xPub: "xpub6CZSUsS4oTrEYic4qasubwoAyw8vS6HYS9GDt2Z6f4jadAsCUijcaqzxytWTjdQ2iGWPhAJUeRc6uCTXenAr624vMwzzzg7mf5KA8h3MNfy"
        addressLength: 1
      }
    }
```
...
```
coins {
      coinCode: "CFX"
      accounts {
        hdPath: "M/44\'/503\'/0\'"
        xPub: "xpub6C5JMtefCmavuYGvzqBEZtoaCY5nLykzpw2yy6M7PRZHe1FixwfNKukmrUBrFL86R1s93dNsrsHxRmMx1NknioeaFdisqsUpfMY9Xs787pZ"
        addressLength: 1
      }
    }
  }
}
coldVersion: 20205
deviceType: "Cobo Vault Pro"

*************************************************************

Most of the above looks safe, but the UUID could potentially
carry our secret key.  The exact format of it needs to be
documented by Cobo, along with a way to validate it.
UUID is a072a758ff78d50b27db92533dd0a3dcbfa92f2825b5a2d65d27e0659c8389ef
```

As one can see, most of the payload is understandable and does not appear to contain any secrets.  However, the UUID is suspicious in that it is not in UUID format (too many bytes!) and is long enough that it could contain one's secret key.

As of today that is where things stand.  I've looked at the [Cobo source code](https://github.com/CoboVault/cobo-vault-cold/) but have not been successful in reverse engineering an independent implementation of decoding the UUID to prove it is safe and not leaking secrets.  Note that [someone else did something similar](https://github.com/CoboVault/cobo-vault-cold/issues/14) and claims that they successfully verified the UUID was safe, but I wasn't able to follow their directions.
