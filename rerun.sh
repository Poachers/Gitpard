#!/usr/bin/env bash

sudo service redis_6379 stop;
sudo service apache2 stop;
sudo service redis_6379 start;
sudo service apache2 start;
sudo supervisorctl reload;