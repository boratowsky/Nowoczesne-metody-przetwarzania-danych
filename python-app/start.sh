#!/bin/bash
pip install flask redis gunicorn
gunicorn -w 4 -b 0.0.0.0:3000 $@
