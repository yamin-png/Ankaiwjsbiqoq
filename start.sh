#!/bin/bash

# Install necessary dependencies
apt-get update
apt-get install -y wget ca-certificates fonts-liberation libappindicator3-1 libasound2 libnss3 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 xdg-utils chromium

# Run your app
gunicorn app:app
