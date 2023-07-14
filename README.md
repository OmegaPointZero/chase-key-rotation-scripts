# Key Rotation Scripts

These scripts are meant to assist and automate in the rotation and testing of the keys used for the Chase integrations.

## Installation

Install the required dependencies with the following:
```
npm i
pip3 install -r requirements.txt
```

## Automated JWK Generation

You will need to copy the DigiCert CA `.crt` file and the new certificate from IT to the current directory. Then run the `generate_jwk.sh` script like so to generate the JWK synchronize the expiration timestamps and adjust the key ID:

```
./generate_jwk.sh <certificate-name> <Digicert-ca> <output-json-filename>
```

## Testing

Once the JWK has been generated, you need to upload your `.yaml` files to the dev, sandbox and live environments, then run the test in the following way, using the `.json` filename for the key you are rotating:

```
python3 test_jwk.py chase-(pan-)jwk.json <dev|sandbox|live> <vault_id>
```

You can then copy the `.json` file to the repo to update the keys on the public website when testing is completed in dev, sandbox and live.
