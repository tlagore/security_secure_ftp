#!/bin/bash

if (( $# != 2)); then
   echo "Improper usage. Usage is $0 [ip] [port]"
   exit
fi

echo "Creating dummy files..."
dd if=/dev/urandom bs=1K iflag=fullblock count=1 > 1KB.bin
dd if=/dev/urandom bs=1K iflag=fullblock count=1K > 1MB.bin
dd if=/dev/urandom bs=1K iflag=fullblock count=256K > 256MB.bin

echo "MD5 checksums in order (1kb, 1mb, 256mb)"
openssl md5 1KB.bin
openssl md5 1MB.bin
openssl md5 256MB.bin

#256MB write
echo "Uploading 256MB.bin md5:"
openssl md5 256MB.bin
cat 256MB.bin | python3 __main__.py write 256MB.bin $1:$2 none
echo ""

echo "Uploading 1MB.bin md5:"
openssl md5 1MB.bin
cat 1MB.bin | python3 __main__.py write 256MB.bin $1:$2 none
echo ""

echo "Downloading 1MB.bin md5:"
openssl md5 1MB.bin
python3 __main__.py read 256MB.bin $1:$2 none > 1MB_copy.bin

echo ""
echo "Md5 comparison: "
echo ""
openssl md5 1MB.bin
openssl md5 1MB_copy.bin
echo ""
