const jose = require('node-jose');
const crypto = require('crypto');
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
		jwks.keys[0].x5c = chain ? [chainvals[0]] : undefined;
		jwks.keys[0].use = "enc";
		jwks.keys[0].alg = "RSA-OAEP-256";
		var sha = crypto.createHash('sha1')
		sha.update(Buffer.from(chainvals[0], 'base64'));
		jwks.keys[0].x5t = sha.digest('base64');;
		jwks.keys[0].expires_on = Date.now() + 60 * 60 * 24 * 1000 * 365;
		console.log(JSON.stringify(jwks, null, 4));
	});
