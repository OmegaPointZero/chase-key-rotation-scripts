import json
import os
import requests
import sys

from jwcrypto import jwe, jwk


def test_pan_key(key, tenant, env):
    to_encrypt = "4111111111111111".encode('utf-8')
    protected_header = {
        "alg": "RSA-OAEP-256", 
        "enc": "A128CBC-HS256",
        "kid": key['kid'],
        "cty": "JWT"
    }
    jwe_enc = jwe.JWE(
        plaintext=to_encrypt,
        protected=protected_header
    )
    jwe_enc.add_recipient(key)
    jwe_string = jwe_enc.serialize(compact=True)

    if env == "dev":
        url = f"https://{tenant}.sandbox.verygoodproxy.io/post"
    elif env == "sandbox":
        url = f"https://{tenant}.sandbox.verygoodproxy.com/post"
    elif env == "live":
        url = f"https://{tenant}.live.verygoodproxy.com/post"

    res = requests.post(url, json={"chase_pan": jwe_string})
    response = json.loads(res.text)
    if response['json']['chase_pan'] != "4111111111111111":
        raise Exception("Error in VGS Decryption attempt, check vault logs.")
    else:
        print("\tValid JWE generated and decrypted.")

def test_payload_key(key, tenant, env):
    to_encrypt = json.dumps({"pan": "4111111111111111"})
    protected_header = protected_header = {
        "alg": "RSA-OAEP-256", 
        "enc": "A256GCM",
        "kid": key['kid']
    }
    jwe_enc = jwe.JWE(
        plaintext=to_encrypt,
        protected=protected_header
    )
    jwe_enc.add_recipient(key)
    jwe_string = jwe_enc.serialize(compact=True)
    if env == "dev":
        url = f"https://{tenant}.sandbox.verygoodproxy.io/post"
    elif env == "sandbox":
        url = f"https://{tenant}.sandbox.verygoodproxy.com/post"
    elif env == "live":
        url = f"https://{tenant}.live.verygoodproxy.com/post"
    res = requests.post(url, json={"chase": jwe_string})
    response = json.loads(res.text)
    if response['json']['chase'] != '{"pan":"4111111111111111"}':
        raise Exception("Error in VGS Decryption attemt, check vault logs.")
    else:
        print("\tValid JWE generated and decrypted.")


def test_jwk(filename, env, vault_id):
    with open(filename, "r") as f:
        new_jwk = json.loads(f.read())['keys'][0]
        new_key = jwk.JWK.from_json(json.dumps(new_jwk))
    url_root = "https://www.verygoodsecurity.com/keys/"
    remote_path = os.path.join(url_root, filename)
    res = requests.get(remote_path)
    old_jwk = json.loads(res.text)['keys'][0]
    old_key = jwk.JWK.from_json(json.dumps(old_jwk))

    if filename == "chase-pan-jwk.json":
        print("Testing the old key...")
        test_pan_key(old_key, vault_id, env)
        print("Testing the new key...")
        test_pan_key(new_key, vault_id, env)
    elif filename == "chase-jwk.json":
        print("Testing the old key...")
        test_payload_key(old_key, vault_id, env)
        print("Testing the new key...")
        test_payload_key(new_key, vault_id, env)

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 4:
        print("Usage:\n$ python3 test_jwk.py <chase-jwk.json|chase-pan-jwk.json> <dev|sandbox|live> <vault_id>")
        print("\nThe .json filename on the website must match the .json filename in this directory (the filename of the new json file you wish to upload)")
    else:
        filenames = ["chase-pan-jwk.json", "chase-jwk.json"]
        if args[1] not in filenames:
            raise Exception(f"Error: filename '{args[1]}' not found in {str(filenames)}, double check to ensure filenames correspond correctly.")
        envs = ["live", "sandbox", "dev"]
        if args[2] not in envs:
            raise Exception(f"Error: environment {args[2]} not found in '{str(envs)}'.")
        test_jwk(args[1], args[2], args[3])





















