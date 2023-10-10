#!/bin/bash

if [ -d .env ]
then
	echo "Enabling virtual env"
else
	echo "No virtual env found. Run local_setup.sh first"
	exit 1
fi

. .env/bin/activate
export ENV=development
export SECRET_KEY="1029384756A"
python app.py
deactivate
