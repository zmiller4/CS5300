#!/usr/bin/env bash

if [ ! -d ~/venv_hw2 ]; then
  python3 -m venv ~/venv_hw2 --system-site-packages
fi
source ~/venv_hw2/bin/activate
python3 -m pip install -q -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:3000