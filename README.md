# pem-to-jwk

Converts a pem-encoded public certificate to a jwk token.

## Automated Usage

Run the `generate_jwk.sh` script like so to automatically install all dependencies, generate the JWK and synchronize the expiration timestamps:

```
./generate_jwk.sh <certificate-name> <Digicert-ca> <output-json-filename>
```

## Dependencies

* nodejs
* npm

Install node dependencies with:
```
npm i
```

## Usage

```
node index.js <certificate-name> [<cert-chain-entry1>, <cert-chain-entry2>, ...]
```

For example:
```
node index.js www_verygoodsecurity_com.crt DigiCertCA.crt TrustedRoot.crt
```
