#!/bin/bash

cd ./frontend/
yarn start &
cd ..
python3 ./backend/manage.py runserver 


