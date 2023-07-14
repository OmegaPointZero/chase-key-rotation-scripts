#!/bin/bash

if [ $# -lt 3 ]
then
    echo "Usage: ./generate_jwk.sh <certificate-name> <digicert-ca> <output-json-filename>"
else
    # npm i
    # pip3 install -r requirements.txt
    node index.js $1 $2 > $3
    python3 fix_jwk.py $3
fi