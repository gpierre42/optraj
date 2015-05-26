#!/bin/sh
HOST='ftp.olikeopen.com'
USER='olope_13980528'
PASSWD='bbpordic'
PORT='21'

echo 'FTPing'
lftp ftp://olope_13980528:bbpordic@ftp.olikeopen.com -e "mirror -e -R htdocs/ /htdocs/ ; quit"


