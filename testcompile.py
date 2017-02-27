import py_compile
import os

py_compile.compile('server/ftp_server.py', cfile='bin/ftp_server.pyc')
py_compile.compile('client/ftp_client.py', cfile='bin/ftp_client.pyc')

#uncomment to remove pyc files on compile
for fileName in os.listdir('bin/'):
    os.remove('bin/' + fileName)
