const jose = require('node-jose');
const fs = require('fs');

const args = process.argv.slice(2);

const key = fs.readFileSync(args[0]);
const chain = args.slice(1)

const keystore = jose.JWK.createKeyStore();
const chainvals = chain.map(file => fs.readFileSync(file, 'ascii'))

keystore
	.add(key, 'pem')
	.then(_ => {
		const jwks = keystore.toJSON();
		jwks.x5c = chain ? chainvals : undefined;
		console.log(JSON.stringify(jwks, null, 4));
	});
