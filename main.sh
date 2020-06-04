#!/bin/bash

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

echo "*******************"
PS3='Select an option and press Enter: '
options=("cppcheck" "flawfinder" "pscan" "frama-c" "scan-build" "sparse" "ikos" "infer")
select opt in "${options[@]}"
do
case $opt in
        "cppcheck")
          sudo apt install -y cppcheck
          cd ~/sastevaluation/juliet_c_13/runners/
	      ./run_cppcheck.sh
          cd ~/sastevaluation/juliet_c_13
	      sudo python3 import_log.py
	      sudo python3 report.py
          break
          ;;
        "flawfinder")
          sudo apt install -y flawfinder
          cd ~/sastevaluation/juliet_c_13/runners/
	      ./run_flawfinder.sh
          cd ~/sastevaluation/juliet_c_13
	      sudo python3 import_log.py
	      sudo python3 report.py
          break
          ;;
        "pscan")
          sudo apt install -y pscan
          cd ~/sastevaluation/juliet_c_13/runners/
          ./run_pscan.sh
          cd ~/sastevaluation/juliet_c_13
	      sudo python3 import_log.py
	      sudo python3 report.py
          break
          ;;
	    "frama-c")
          sudo apt install -y frama-c
          cp -r ~/sastevaluation/C/testcasesupport ~/sastevaluation/juliet_c_13/runners/
          cd ~/sastevaluation/juliet_c_13/runners/
	      ./run_framac.sh
          cd ~/sastevaluation/juliet_c_13
          sudo python3 import_log.py
	      sudo python3 report.py
          rm -r ~/sastevaluation/juliet_c_13/runners/testcasesupport
          break
          ;;
	    "scan-build")
          pip3 install scan-build
          cd ~/sastevaluation/juliet_c_13/runners/
	      ./run_scan-build.sh
          mv ~/sastevaluation/C/scan-build-results.log ~/sastevaluation/juliet_c_13/runners
          cd ~/sastevaluation/juliet_c_13
	      sudo python3 import_log.py
	      sudo python3 report.py
          break
          ;;
	    "sparse")
	      sudo apt install -y sparse
          cp -r ~/sastevaluation/C/testcasesupport ~/sastevaluation/juliet_c_13/runners/
          cd ~/sastevaluation/juliet_c_13/runners/
	      ./run_sparse.sh
          cd ~/sastevaluation/juliet_c_13
	      sudo python3 import_log.py
	      sudo python3 report.py
          rm -r ~/sastevaluation/juliet_c_13/runners/testcasesupport
          break
          ;;
	    "ikos")
          ./install_ikos.sh
          cp -r ~/sastevaluation/C/testcasesupport ~/sastevaluation/juliet_c_13/runners/
          cp -r ~/sastevaluation/C/testcases ~/sastevaluation/juliet_c_13/runners/
          cd ~/sastevaluation/juliet_c_13/runners/
	      ./run_ikos.sh
          cd ~/sastevaluation/juliet_c_13
	      sudo python3 import_log.py
	      sudo python3 report.py
          rm -r ~/sastevaluation/juliet_c_13/runners/testcasesupport
          rm -r ~/sastevaluation/juliet_c_13/runners/testcases
          break
          ;;
	    "infer")
          cd sastevaluation
          wget https://github.com/facebook/infer/releases/download/v0.17.0/infer-linux64-v0.17.0.tar.xz
          tar -zxvf infer-linux64-v0.17.0.tar.xz && rm infer-linux64-v0.17.0.tar.xz
          cp -r ~/sastevaluation/C/testcasesupport ~/sastevaluation/juliet_c_13/runners/
          cp -r ~/sastevaluation/C/testcases ~/sastevaluation/juliet_c_13/runners/
          cd ~/sastevaluation/juliet_c_13/runners/
	      ./run_infer.sh
          cd ~/sastevaluation/juliet_c_13
	      sudo python3 import_log.py
	      sudo python3 report.py
          rm -r ~/sastevaluation/juliet_c_13/runners/testcasesupport
          rm -r ~/sastevaluation/juliet_c_13/runners/testcases
          break
          ;;
        *) echo "invalid option";;
  esac
done
echo -e "###################################################################################### "
echo -e "###################################################################################### "
echo -e "Evaluation Complete"
echo -e "###################################################################################### "
echo -e "###################################################################################### "










