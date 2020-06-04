#!/bin/bash

#----------------------------------------
#author:  Rohan Krishnamurthy, 
#rohan.krishnamurthy@dlr.de
#German Aerospace Center
#Year 2020
#----------------------------------------

echo -e "###################################################################################### "
echo -e "###################################################################################### "
echo -e "Choice of tools for Evaluation"
echo -e "###################################################################################### "
echo -e "###################################################################################### "


echo "*******************"
PS3='Select an option and press Enter: '
options=("cppcheck" "flawfinder" "pscan" "frama-c" "scan-build" "sparse" "ikos" "infer" "oclint" "adlint")
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
        "oclint")
          cd sastevaluation
          wget https://github.com/oclint/oclint/releases/download/v0.13.1/oclint-0.13.1-x86_64-linux-4.4.0-112-generic.tar.gz 
          tar -zxvf oclint-0.13.1-x86_64-linux-4.4.0-112-generic.tar.gz && rm oclint-0.13.1-x86_64-linux-4.4.0-112-generic.tar.gz
          cp -r ~/sastevaluation/C/testcasesupport ~/sastevaluation/juliet_c_13/runners/
          cd ~/sastevaluation/juliet_c_13/runners/
          ./run_oclint.sh
          cd ~/sastevaluation/juliet_c_13
          sudo python3 import_log.py
          sudo python3 report.py
          break
          ;;
       "adlint")
          cd sastevaluation
          sudo apt-get install gcc-6
          sudo apt install ruby-full
          sudo gem install adlint --no-ri --no-rdoc
          cp -r ~/sastevaluation/C/testcasesupport ~/sastevaluation/juliet_c_13/runners/
          cd ~/sastevaluation/juliet_c_13/runners/
          ./run_adlint.sh
          cd ~/sastevaluation/juliet_c_13
          sudo python3 import_log.py
          sudo python3 report.py
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

