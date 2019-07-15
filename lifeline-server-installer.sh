#!/usr/bin/env bash

dir=$(pwd)

# grap OS from os-release (ex. ID="centos")
eval $(cat /etc/os-release | grep ^ID=.*)

echo "Installing from github"
mkdir /opt/lifeline /opt/lifeline/temperatures /opt/lifeline/elasticsearch /opt/lifeline/grafana
curl https://raw.githubusercontent.com/bmswens/lifeline/master/lifeline/lifeline.py > /opt/lifeline/lifeline.py
curl https://raw.githubusercontent.com/bmswens/lifeline/master/lifeline/lifeline.yml > /opt/lifeline.yml
curl https://raw.githubusercontent.com/bmswens/lifeline/master/lifeline/lifeline.sh > /opt/lifeline.sh
curl https://raw.githubusercontent.com/bmswens/lifeline/master/lifeline/temperatures/$ID.py > \
     /opt/lifeline/temperatures/$ID.py
curl https://raw.githubusercontent.com/bmswens/lifeline/master/lifeline/docker-compose.yml > \
     /opt/lifeline/docker-compose.yml
curl https://raw.githubusercontent.com/bmswens/lifeline/master/requirments.txt > /opt/lifeline/requirments.txt

echo "Creating venv"
python3 -m venv /opt/lifeline/lifeline-venv
source /opt/lifeline/lifeline-venv/bin/activate
pip3 install -r /opt/lifeline/requirments.txt
deactivate

echo "Starting docker images"
cd /opt/lifeline
chown 472:472 /opt/lifeline/grafana
chmod 777 /opt/lifeline/elasticsearch
docker-compose up -d
cd $(dir)

echo "Done installing."
echo "Please edit /opt/lifeline-pi/lifeline.yml with your config."
echo "Please add * * * * * /opt/lifeline-pi/lifeline.sh to your crontab."
