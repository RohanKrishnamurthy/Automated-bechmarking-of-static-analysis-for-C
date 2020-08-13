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
options=("cppcheck" "flawfinder" "clang-tidy" "pscan" "frama-c" "scan-build" "sparse" "ikos" "infer" "oclint" "adlint")
select opt in "${options[@]}"
do
case $opt in
        "cppcheck")
          sudo apt install -y cppcheck
          cd ~/sastevaluation/juliet_c_13/runners/
	  ./run_cppcheck.sh
          break
          ;;
        "flawfinder")
          sudo apt install -y flawfinder
          cd ~/sastevaluation/juliet_c_13/runners/
	  ./run_flawfinder.sh
          break
          ;;
	 "clang-tidy")
	   sudo apt install -y clang-tidy-4.0
	   cd ~/sastevaluation/juliet_c_13/runners/
	   chmod +x run_clang_tidy.sh
	  ./run_clang_tidy.sh
          break
          ;;
        "pscan")
          sudo apt install -y pscan
          cd ~/sastevaluation/juliet_c_13/runners/
          ./run_pscan.sh
          break
          ;;
	    "frama-c")
          sudo apt install -y frama-c
          cp -r ~/sastevaluation/C/testcasesupport ~/sastevaluation/juliet_c_13/runners/
          cd ~/sastevaluation/juliet_c_13/runners/
    	  ./run_framac.sh
          break
          ;;
	    "scan-build")
          sudo apt install -y clang-tools-4.0
          cd ~/sastevaluation/juliet_c_13/runners/
	  ./run_scan-build.sh
          mv ~/sastevaluation/C/scan-build-results.log ~/sastevaluation/juliet_c_13/runners
          break
          ;;
	    "sparse")
	      sudo apt install -y sparse
          cp -r ~/sastevaluation/C/testcasesupport ~/sastevaluation/juliet_c_13/runners/
          cd ~/sastevaluation/juliet_c_13/runners/
          ./run_sparse.sh
          break
          ;;
	    "ikos")
	  cd ~/sastevaluation/juliet_c_13/runners/
	  chmod +x install_ikos.sh
          ./install_ikos.sh
          cp -r ~/sastevaluation/C/testcasesupport ~/sastevaluation/juliet_c_13/runners/
          cp -r ~/sastevaluation/C/testcases ~/sastevaluation/juliet_c_13/runners/
          cd ~/sastevaluation/juliet_c_13/runners/
          ./run_ikos.sh
          break
          ;;
	    "infer")
          cd sastevaluation
          wget https://github.com/facebook/infer/releases/download/v0.17.0/infer-linux64-v0.17.0.tar.xz
          tar -xvJf infer-linux64-v0.17.0.tar.xz && rm infer-linux64-v0.17.0.tar.xz
          cp -r ~/sastevaluation/C/testcasesupport ~/sastevaluation/juliet_c_13/runners/
          cp -r ~/sastevaluation/C/testcases ~/sastevaluation/juliet_c_13/runners/
          cd ~/sastevaluation/juliet_c_13/runners/
	  ./run_infer.sh
          break
          ;;
        "oclint")
          cd sastevaluation
          wget https://github.com/oclint/oclint/releases/download/v0.13.1/oclint-0.13.1-x86_64-linux-4.4.0-112-generic.tar.gz 
          tar -zxvf oclint-0.13.1-x86_64-linux-4.4.0-112-generic.tar.gz && rm oclint-0.13.1-x86_64-linux-4.4.0-112-generic.tar.gz
          cp -r ~/sastevaluation/C/testcasesupport ~/sastevaluation/juliet_c_13/runners/
          cd ~/sastevaluation/juliet_c_13/runners/
          ./run_oclint.sh
          break
          ;;
       "adlint")
          sudo apt-get install gcc-6
          sudo apt install ruby-full
          sudo gem install adlint --no-ri --no-rdoc
          cp -r ~/sastevaluation/C/testcasesupport ~/sastevaluation/juliet_c_13/runners/
          cd ~/sastevaluation/juliet_c_13/runners/
          ./run_adlint.sh
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

