#!/bin/bash

# Regular Colors
Black='\033[0;30m'        # Black
Red='\033[0;31m'          # Red
Green='\033[0;32m'        # Green
Yellow='\033[0;33m'       # Yellow
Blue='\033[0;34m'         # Blue
Purple='\033[0;35m'       # Purple
Cyan='\033[0;36m'         # Cyan
White='\033[0;37m'        # White
reset='\033[0m'       # Text Reset

VERSION="v1.0"
rootCA="NanobrokCA"
serverCA="serverNB"

display_help() {
    echo "Usage: $0 <argument>" >&2
    echo "Example: "
    echo -e "$0 domains.ext"
    exit 1
}

echo -e "Nanobrok Certificate authority (CA) generator"
echo -e "Version: $VERSION\n"

if [ -z "$1" ]; then
    display_help
    exit 1
fi

domains="$1"

if [ ! -f "$domains" ]; then
    echo -e "${Red}ERROR: ${reset}The file $domains not found!"
    echo -e "${Red}ERROR: ${reset} First, create a file domains.ext that lists all your local domains"
    exit 1
fi

if ! command -v 'openssl' &> /dev/null
then
    echo -e "${Yellow}Openssl: ${reset} openssl could not be found"
    exit
fi

echo -e "${Yellow}Openssl: ${reset} Generate root (CA) ${rootCA}.pem, ${rootCA}.key & ${rootCA}.crt"
openssl req -x509 -nodes -new -sha256 -days 1024 -newkey rsa:2048 -keyout ${rootCA}.key -out ${rootCA}.pem -subj "/C=US/CN=Nanobrok-Server-CA"
openssl x509 -outform pem -in ${rootCA}.pem -out ${rootCA}.crt

echo -e "${Yellow}Openssl: ${reset} Generate server (CA) ${serverCA}.key and ${serverCA}.csr"
openssl req -new -nodes -newkey rsa:2048 -keyout ${serverCA}.key -out ${serverCA}.csr -subj "/C=US/ST=State/L=City/O=Example-Certificates/CN=Nanobrok.server"
openssl x509 -req -sha256 -days 1024 -in ${serverCA}.csr -CA ${rootCA}.pem -CAkey ${rootCA}.key -CAcreateserial -extfile $domains -out ${serverCA}.crt
echo -e "${Blue}Info: ${reset} The self-signed certificates has been generated successfully."
