#!/bin/sh

set -eu

python manage.py migrate
python manage.py create_local_admin