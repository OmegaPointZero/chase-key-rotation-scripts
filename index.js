const jose = require('node-jose');
const fs = require('fs');

const args = process.argv.slice(2);

const key = fs.readFileSync(args[0]);
const chain = args.slice(1)

const keystore = jose.JWK.createKeyStore();
const chainvals = chain.map(file => fs.readFileSync(file, 'ascii'))

for(var i=0;i<chainvals.length;i++){
    chainvals[i] = chainvals[i].split('\n').slice(1,-2).join('')
}

keystore
    .add(key, 'pem')
    .then(_ => {
        const jwks = keystore.toJSON();
        jwks.keys[0].x5c = chain ? chainvals : undefined;
        jwks.keys[0].use = "enc";
        jwks.keys[0].alg = "RSA-OAEP";
        jwks.keys[0].expires_on = 2222222222;
        console.log(JSON.stringify(jwks, null, 4));
    });