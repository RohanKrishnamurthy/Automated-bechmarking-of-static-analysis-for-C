#!/bin/bash

#----------------------------------------
#author:  Rohan Krishnamurthy, 
#rohan.krishnamurthy@dlr.de
#German Aerospace Center
#Year 2020
#----------------------------------------


echo -e "###################################################################################### "
echo -e "INSTALLING pre-requisits "
echo -e "###################################################################################### "

sudo apt -y update
sudo apt install -y git
sudo apt install -y python2.7
sudo apt install -y python3.6
sudo apt install -y python-pip
sudo apt install -y python3-pip
sudo apt install -y python3-mysqldb
sudo apt install -y python-mysqldb
pip3 install numpy
pip install numpy


echo -e "###################################################################################### "
echo -e "Downloading and Extracting the test_Suite"
echo -e "###################################################################################### "

sudo apt install wget
wget https://samate.nist.gov/SARD/testsuites/juliet/Juliet_Test_Suite_v1.3_for_C_Cpp.zip
unzip Juliet_Test_Suite_v1.3_for_C_Cpp.zip && rm Juliet_Test_Suite_v1.3_for_C_Cpp.zip

echo -e "###################################################################################### "
echo -e "Building the makefile "
cd C && make
echo -e "###################################################################################### "

echo -e "###################################################################################### "
echo -e "Install-Start-Enable Mysql"
echo -e "###################################################################################### "
sudo apt -y update
sudo apt install -y mysql-server

sudo apt -y install expect

MYSQL_ROOT_PASSWORD=root

SECURE_MYSQL=$(sudo expect -c "
set timeout 10

spawn mysql_secure_installation

expect \"Enter current password for root (enter for none):\"
send \"$MYSQL_ROOT_PASSWORD\r\"

expect \"Enter re-enter password for root (enter for none):\"
send \"$MYSQL_ROOT_PASSWORD\r\"

expect \"Change the root password?\"
send \"y\r\"

expect \"Remove anonymous users?\"
send \"y\r\"

expect \"Disallow root login remotely?\"
send \"y\r\"

expect \"Remove test database and access to it?\"
send \"y\r\"

expect \"Reload privilege tables now?\"
send \"y\r\"

expect eof
")

echo "${SECURE_MYSQL}"
sudo apt -y purge expect

sudo ufw allow mysql
sudo systemctl start mysql
sudo systemctl enable mysql
sudo mysql -u root -proot --execute="create database samate; use samate; source database.sql;"

echo -e "###################################################################################### "
echo -e "Initiation Complete"
echo -e "###################################################################################### "
