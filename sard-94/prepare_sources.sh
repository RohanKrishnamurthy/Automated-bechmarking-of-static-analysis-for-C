#!/usr/bin/env bash

git clone https://code.wireshark.org/review/wireshark

cd wireshark

git checkout "v1.8.0"

patch < wireshark.patch

./autogen.sh

./configure

bear make -j4