#!/bin/bash

export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_APP=SISUKIT
export FLASK_ENV=development
nohup flask run -h 0.0.0.0 -p 8080 &
