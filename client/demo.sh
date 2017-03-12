#!/bin/bash

if (( $# != 3)); then
   echo "Improper usage. Usage is $0 [ip] [port] [output_filename]"
   exit
fi

dd if=/dev/urandom bs=1K iflag=fullblock count=1 > 1KB.bin
dd if=/dev/urandom bs=1K iflag=fullblock count=1K > 1MB.bin
dd if=/dev/urandom bs=1K iflag=fullblock count=256K > 256MB.bin

openssl md5 1KB.bin
openssl md5 1MB.bin
openssl md5 256MB.bin

#256MB write
echo "Uploading 256MB.bin"
#cat 256MB.bin | python3 __main__.py write 256MB.bin $1:$2 none

echo "Uploading 1MB.bin"
#cat 1MB.bin | python3 __main__.py write 256MB.bin $1:$2 none


:'
{ time cat 1KB.bin | python3 __main__.py write 1KB.bin $1:$2 none; } 2>> $3
{ time cat 1KB.bin | python3 __main__.py write 1KB.bin $1:$2 aes128 helloworldhellow; } 2>> $3
{ time cat 1KB.bin | python3 __main__.py write 1KB.bin $1:$2 aes256 helloworldhellow; } 2>> $3

#1KB read
echo "Testing 1KB read"
{ time python3 __main__.py read 1KB.bin $1:$2 none > 1KB.bin; } 2>> $3
{ time python3 __main__.py read 1KB.bin $1:$2 aes128 helloworldhellow > 1KB.bin; } 2>> $3
{ time python3 __main__.py read 1KB.bin $1:$2 aes256 helloworldhellow > 1KB.bin; } 2>> $3

#1MB write
echo "Testing 1MB write"
{ time cat 1MB.bin | python3 __main__.py write 1MB.bin $1:$2 none; } 2>> $3
{ time cat 1MB.bin | python3 __main__.py write 1MB.bin $1:$2 aes128 helloworldhellow; } 2>> $3
{ time cat 1MB.bin | python3 __main__.py write 1MB.bin $1:$2 aes256 helloworldhellow; } 2>> $3

#1MB read
echo "Testing 1MB read"
{ time python3 __main__.py read 1MB.bin $1:$2 none > 1MB.bin; } 2>> $3
{ time python3 __main__.py read 1MB.bin $1:$2 aes128 helloworldhellow > 1MB.bin; } 2>> $3
{ time python3 __main__.py read 1MB.bin $1:$2 aes256 helloworldhellow > 1MB.bin; } 2>> $3

#1GB write
echo "Testing 1GB write"
{ time cat 1GB.bin | python3 __main__.py write 1GB.bin $1:$2 none; } 2>> $3
{ time cat 1GB.bin | python3 __main__.py write 1GB.bin $1:$2 aes128 helloworldhellow; } 2>> $3
{ time cat 1GB.bin | python3 __main__.py write 1GB.bin $1:$2 aes256 helloworldhellow; } 2>> $3

#1GB read
echo "Testing 1GB read"
{ python3 __main__.py read 1GB.bin $1:$2 none > 1GB.bin; } 2>> $3
{ python3 __main__.py read 1GB.bin $1:$2 aes128 helloworldhellow > 1GB.bin; } 2>> $3
{ python3 __main__.py read 1GB.bin $1:$2 aes256 helloworldhellow > 1GB.bin; } 2>> $3

echo "Test suite finished"
'
