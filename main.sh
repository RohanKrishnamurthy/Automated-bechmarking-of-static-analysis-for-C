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

sudo apt update
sudo apt install -y git
sudo apt install python2.7
sudo apt install python3.6
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
sudo apt update
sudo apt install -y mysql-server
sudo mysql_secure_installation utility
#Note: You will be prompted to validate the password.
#1. Hit y|Y
#2. Choose the strength of the password: 0-1-2
#3. Enter New password: root
#4. Re-enter  new password: root
#5. Hit y|Y to continue
#6. Remove anonymous users? : Hit y|Y
#7. Disallow root login remotely? : Hit y|Y
#8. Remove test database and access to it? : Hit y|Y
#9. Reload privlege tables now? : Hit y|Y
#10. All done!
sudo ufw allow mysql
sudo systemctl start mysql
sudo systemctl enable mysql
sudo mysql -u root -p --execute="create database samate; use samate; source database.sql;"
#Note: Enter Password: root
echo -e "database uploaded successfully"
echo -e "###################################################################################### "
echo -e "###################################################################################### "
echo -e "Initiation Complete"
echo -e "###################################################################################### "
echo -e "###################################################################################### "










