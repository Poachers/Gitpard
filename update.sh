#!/usr/bin/env bash

cd $PWD

href_commits='https://bitbucket.org/poachers/gitpard/commits/'
href_issues='https:\/\/bitbucket.org\/poachers\/gitpard\/issues\/'

echo '<h3><a href="/">home</a></h3>';
echo "<code>===============================";
echo "========== git pull ===========";
echo "===============================</br>";
git pull;
echo;
git log -1 --pretty=format:"<a href=\"$href_commits%H\">%h</a>: ";
git log -1 --pretty=format:"%s" | sed "s/\(#\([1-9][0-9]*\)*\)*\(.*\)/<a href=\"$href_issues\2\">\1<\/a>\3/g";
git log -1 --pretty=format:"</br>%ar</br>%an &lt;%ce&gt;</br></br>";
echo "===============================";
echo "===== ./manage.py migrate =====";
echo "===============================</br>";
./manage.py migrate;
echo "</code>";
sudo service redis_6379 stop;
sudo service apache2 stop;
sudo service redis_6379 start;
sudo service apache2 start;
sudo supervisorctl reload;