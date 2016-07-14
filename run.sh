#!/bin/sh
pip install -r requirements.txt
mongod &
python telebot.py &
