#!/bin/sh
#Install lua5
apt-get install lua5.2
#Lua Rocks
git clone https://github.com/torch/distro.git ~/torch --recursive
cd ~/torch; bash install-deps;
./install.sh

#char rnn deps
luarocks install nngraph
luarocks install optim
luarocks install nn
