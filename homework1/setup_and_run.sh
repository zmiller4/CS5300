#!/usr/bin/env bash

if [ ! -d ~/hw1 ]; then
  python3 -m venv ~/hw1
fi
source ~/hw1/bin/activate
python3 -m pip install -q pytest httpx
python ./run_all.py

