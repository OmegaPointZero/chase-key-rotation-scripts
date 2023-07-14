import json
import base64
import requests
import sys
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from datetime import datetime

def adjust_attributes(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    first_key = data['keys'][0]
    x5c = first_key['x5c'][0]
    cert_der = base64.b64decode(x5c)
    cert = x509.load_der_x509_certificate(cert_der, default_backend())
    exp_date = cert.not_valid_after
    timestamp = int(exp_date.timestamp())
    first_key['expires_on'] = timestamp

    new_key_id = first_key['kid']
    if "validate.verygoodsecurity.com" in new_key_id:
        # validate.verygoodsecurity.com is the chase-pan-jwk.json file
        res = requests.get("https://verygoodsecurity.com/keys/chase-pan-jwk.json")
    elif "www.verygoodsecurity.com" in new_key_id:
        # this is the chase-jwk.json file
        res = requests.get("https://verygoodsecurity.com/keys/chase-jwk.json")

    response_json = json.loads(res.text)["keys"][0]
    if new_key_id == response_json['kid']:
        print("Same key ID, rotating Key IDs for new key...")
        if new_key_id[-2] == ".2":
            new_key_id = new_key_id[:-2]
        else:
            new_key_id = new_key_id + ".2"

        print(f"Old key ID: {response_json['kid']}\nNew Key ID: {new_key_id}")
    else:
        print(f"Key IDs are different: {response_json['kid']} != {response_json['kid']}")

    data['keys'][0]['kid'] = new_key_id

    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    file_name = sys.argv[1]
    adjust_attributes(file_name)
