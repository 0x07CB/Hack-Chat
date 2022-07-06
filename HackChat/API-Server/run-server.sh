#!/bin/bash
cd /etc/hackchat/ && sudo gunicorn -b '0.0.0.0':'4344' --workers=2 "API:create_app()"