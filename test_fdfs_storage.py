#/usr/bin/env  python
""" this script main to check the fdfs storage basic function is ok  or not
    before run this script, you must make /root/test file exist. and modify the
	${FDFS}/etc/client.conf 
	tracker_server_ip ,comment base_path 
"""
import os
import hashlib
import socket
import re
import subprocess
from subprocess import Popen,PIPE
print "Get host ip information"
ip=os.system("ip a s dev bond0|awk '/scope global bond0/{sub(/ .*inet /,\"\",$0);sub(/\/16 brd .*/,\"\",$0);print }'")
DIR="/usr/local/fastdfs/"
CMD=DIR+"/bin/fdfs_upload_file"
CONF_FILE=DIR+"/etc/client.conf"
LOCAL_FILE_NAME="/root/test"
print "Get file hashlib Section"
#ufkeys=hashlib.md5(fname_string)
#ufkeys=key.update(LOCAL_FILE_NAME)
print "upload test file to server "
p=subprocess.Popen([" %s %s %s %s:23000" % (CMD,CONF_FILE,LOCAL_FILE_NAME,ip)],stdout=subprocess.PIPE, shell=True)
p_return=p.poll()
(out, err) = p.communicate()
print out
fname=out.split('/')
fname_string=fname[-1].strip()
finame=re.sub('group\d+/','',out)
print "Get file hashlib Section"
ufkeys=hashlib.md5(open(LOCAL_FILE_NAME).read()).hexdigest()
#ufkeys=key.update(LOCAL_FILE_NAME)
if p:
        print "we can upload file to server"
else:
        print "we can't upload file to server"
        exit
print "echo check download function"
ip=os.system("ip a s dev bond0|awk '/scope global bond0/{sub(/ .*inet /,\"\",$0);sub(/\/16 brd .*/,\"\",$0);print }'")
d=subprocess.Popen([" wget http://%s:29119/%s" % (ip,out)],stdout=subprocess.PIPE, shell=True)
d_return=d.poll()
(dout,derr)=d.communicate()
if not d_return:
        print "we can download the file"
else:
        print "we can't download the file"
        exit
print "check test file hashlib information"
dfkeys=hashlib.md5(open(fname_string).read()).hexdigest()
#dfkeys=newkey.update(fname_string)
print dfkeys
print ufkeys
print "compare hashlib keys"
if ufkeys == dfkeys:
        print "the file is identify"
else:
        print "the fille isn't identify"
        exit
print "echo check file figure print information"
f=subprocess.Popen([" curl -I http://%s:28717/fileinfo/%s" % (ip,finame)],stdout=subprocess.PIPE, shell=True)
f_return=f.wait()
print f_return
print "Here========================"
(fout,ferr)=f.communicate()
if f_return == 0:
        print "good, the figure print info is ok"
else:
        print "the figure print info doesn't OK"
        exit
print "echo check file mediainfo information"
m=subprocess.Popen([" curl -I -XGET 'http://%s:28717/py/mediainfo?path=%s&fileid=test'" % (ip,finame)],stdout=subprocess.PIPE, shell=True)
m_return=m.wait()
(mout,merr)=m.communicate()
if m_return == 0:
        print "good, the figure print info is ok"
else:
        print "the figure print info doesn't OK"
        exit
