#!/usr/bin/env bash

set -a
source .env
set +a

FLASK_APP=manage.py flask run --host=0.0.0.0 --port=8081 --debug