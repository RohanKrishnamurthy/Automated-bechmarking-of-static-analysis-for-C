#!/bin/bash

echo -e "###################################################################################### "
echo -e "INSTALLING IKOS Tool "
echo -e "###################################################################################### "
sudo apt install -y doxygen
sudo apt install -y libcgal-dev
sudo apt install -y libcgal-demo
echo "deb http://apt.llvm.org/bionic/ llvm-toolchain-bionic-9 main" | sudo tee -a /etc/apt/sources.list
wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | sudo apt-key add -
sudo apt-get -y update
sudo apt-get install -y gcc g++ cmake libgmp-dev libboost-dev libboost-filesystem-dev libboost-thread-dev libboost-test-dev python python-pygments libsqlite3-dev libtbb-dev libz-dev libedit-dev llvm-9 llvm-9-dev llvm-9-tools clang-9
wget https://github.com/NASA-SW-VnV/ikos/releases/download/v2.0/ikos-2.0.tar.gz
tar -zxvf ikos-2.0.tar.gz && rm ikos-2.0.tar.gz
cd ikos-2.0
mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX="~/ikos-2.0"
cmake .. -DLLVM_CONFIG_EXECUTABLE="/usr/lib/llvm-9/bin/llvm-config"
make 
make install
make clean
echo -e "###################################################################################### "



