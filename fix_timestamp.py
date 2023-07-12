import json
import base64
import sys
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from datetime import datetime

def update_expiration_timestamp(file_name):
    # Open the file and load the JSON
    with open(file_name, 'r') as f:
        data = json.load(f)

    # Get the first key from the "keys" list
    first_key = data['keys'][0]

    # Get the x5c attribute
    x5c = first_key['x5c'][0]

    # Base64 decode the x5c attribute and parse the X.509 certificate
    cert_der = base64.b64decode(x5c)
    cert = x509.load_der_x509_certificate(cert_der, default_backend())

    # Get the expiration date and convert it to a 10-digit Unix timestamp
    exp_date = cert.not_valid_after
    timestamp = int(exp_date.timestamp())
    
    # Update the "expires_on" value in the first key
    first_key['expires_on'] = timestamp

    # Write the updated JSON back to the file
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    file_name = sys.argv[1]
    update_expiration_timestamp(file_name)
