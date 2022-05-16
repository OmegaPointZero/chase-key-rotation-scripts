const jose = require('node-jose');
const fs = require('fs');

const chain = process.argv.slice(2);

const key = fs.readFileSync(chain[0]);

const keystore = jose.JWK.createKeyStore();
const chainvals = chain.map(file =>
	fs.readFileSync(file, 'ascii').split(/\r?\n/).slice(1, -2).join('')
)

keystore
	.add(key, 'pem')
	.then(_ => {
		const jwks = keystore.toJSON();
		jwks.keys[0].x5c = chain ? chainvals : undefined;
		jwks.keys[0].use = "enc";
		jwks.keys[0].alg = "RSA-OAEP-256";
		jwks.keys[0].expires_on = 2222222222; // Non-standard -- required by Chase.
		console.log(JSON.stringify(jwks, null, 4));
	});
