#!/bin/bash

if [ $# -lt 3 ]
then
    echo "Usage: ./generate_jwk.sh <certificate-name> <digicert-ca> <output-json-filename>"
else
    npm i
    pip3 install -r requirements.txt
    echo "Generating JWK"
    node index.js $1 $2 > $3
    echo "Done."
    echo "Adjusting timestamp."
    python3 fix_timestamp.py $3
    echo "Done. File written to $3."
fi