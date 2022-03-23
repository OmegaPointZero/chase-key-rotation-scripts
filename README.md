# pem-to-jwk

Converts a pem-encoded public certificate to a jwk token.

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
