#!/bin/bash
echo "Setting up Local env"

if [ -d ".env" ]
then
	echo ".env already exists. Installing using pip"
else
	echo "creating .env and installing using pip"
	python3 -m venv .env
fi

#Activate the env
. .env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

deactviate
