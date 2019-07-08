#!/usr/bin/env bash

echo "Installing files from github"
mkdir /opt/lifeline-pi/
curl https://raw.githubusercontent.com/bmswens/lifeline/master/lifeline-pi/lifeline.py > /opt/lifeline-pi/lifeline.py
curl https://raw.githubusercontent.com/bmswens/lifeline/blob/master/lifeline-pi/lifeline.sh > /opt/lifeline-pi/lifeline.sh
curl https://raw.githubusercontent.com/bmswens/lifeline/blob/master/lifeline-pi/lifeline.yml > /opt/lifeline-pi/lifeline.yml
chmod 755 /opt/lifeline-pi/lifeline.sh
chmod 766 /opt/lifeline-pi/lifeline.yml

echo "Creating venv"
python3 -m venv /opt/lifeline-pi/lifeline-venv
source /opt/lifeline-pi/lifeline-venv/bin/activate
pip3 install pyyaml elasticsearch
deactivate

echo "Done installing."
echo "Please edit /opt/lifeline-pi/lifeline.yml with your config."
echo "Please add * * * * * /opt/lifeline-pi/lifeline.sh to your crontab."