#!/bin/bash
echo "Installing dependencies to test module A"
wget https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-linux64.tar.gz
tar -xvzf geckodriver*
chmod +x geckodriver
sudo mv geckodriver /usr/local/bin
rm geckodriver-v0.18.0-linux64.tar.gz
