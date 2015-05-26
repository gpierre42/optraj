#!/bin/bash
 
sudo apt-get remove phantomjs
 
sudo unlink /usr/local/bin/phantomjs
sudo unlink /usr/local/share/phantomjs
sudo unlink /usr/bin/phantomjs
 
cd /usr/local/share
 
sudo wget https://phantomjs.googlecode.com/files/phantomjs-1.9.0-linux-x86_64.tar.bz2
 
tar xjf phantomjs-1.9.0-linux-x86_64.tar.bz2
 
sudo ln -s /usr/local/share/phantomjs-1.9.0-linux-x86_64/bin/phantomjs /usr/local/share/phantomjs; sudo ln -s /usr/local/share/phantomjs-1.9.0-linux-x86_64/bin/phantomjs /usr/local/bin/phantomjs; sudo ln -s /usr/local/share/phantomjs-1.9.0-linux-x86_64/bin/phantomjs /usr/bin/phantomjs
 
phantomjs -v