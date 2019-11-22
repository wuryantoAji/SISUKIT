#!/bin/bash

export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_APP=SISUKIT
export FLASK_ENV=development
nohup flask run -h 10.119.105.15 -p 8080 &
