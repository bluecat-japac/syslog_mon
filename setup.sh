#! /bin/bash

sysconfig="/etc/sysconfig"
file="/etc/sysconfig/syslog-ng"
python_path='$PYTHONPATH'
scl="/usr/share/syslog-ng/include/scl/syslog_mon/"
log="/var/log/mon-app"

# Check if destination directory is existed
if [ ! -z $1 ]
then
  des_path=$1
  if [ ! -d $1 ]
  then
    mkdir -p $1
  fi
else
  des_path="/opt/"
fi

# Copy syslog_monitoring to specific directory
cp -R syslog_monitoring/ $des_path

# Install requirements
cd "$des_path/syslog_monitoring/"
pip install wheel && pip install -r requirements.txt
yes | apt-get install syslog-ng-mod-python
    
# Create sysconfig folder if it doesn't exist
mkdir -p $sysconfig

# Export path of the python destination
echo "PYTHONPATH=$python_path:$des_path/syslog_monitoring/" >> $file

# Copy filters.conf file to scl folder
mkdir $scl
cp "filters.conf" $_

# Create directory to store logs
mkdir $log

# Disable firewall for the bdds to be able to send trap
PsmClient node set firewall-enable=0

# Restart syslog-ng service
service syslog-ng restart
