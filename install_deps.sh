#!/bin/sh
#Install lua5
apt-get install lua5.1
apt-get install liblua5.1-0-dev
#Lua Rocks
git clone https://github.com/torch/distro.git ~/torch --recursive
cd ~/torch; bash install-deps;
./install.sh
source ~/.bashrc

#char rnn deps
luarocks install nngraph
luarocks install optim
luarocks install nn
