# coding=utf-8

import os
import sys
import time
import math
import random
import string
import operator
import commands
from PIL import Image
from hashlib import md5
from qiniu import Auth, put_file, etag

pngpaste = '/usr/local/bin/pngpaste'
if len(sys.argv) == 2:
    pngpaste = sys.argv[1]

ak = YOUR_AK 
sk = YOUR_SK
domain = YOUR_DOAMIN # 例如:'http://7xpx6h.com1.z0.glb.clouddn.com'
bucket = YOUR_BUCKET # 空间名称
q = Auth(ak, sk)

# check pngpaste is exists
re = os.system(pngpaste)
if re == 127:
    print 'command:%s' % pngpaste, 'not exists'
    sys.exit(1)


def image_similar(image1, image2):
    temp1 = Image.open(image1)
    temp2 = Image.open(image2)
    h1 = temp1.histogram()
    h2 = temp2.histogram()
    rms = math.sqrt(reduce(operator.add,  list(map(lambda a,b: (a-b)**2, h1, h2)))/len(h1) )
    print 'two image similar is:', rms
    return rms


def upload_file(upload_file_name, temp):
    key = md5(str(time.time())+''.join(random.sample(string.letters, 12))).hexdigest()
    mime_type = 'image/png'
    token = q.upload_token(bucket, key)
    ret, info = put_file(token, key, upload_file_name, mime_type=mime_type, check_crc=True)
    print 'upload qiniu result:', info
    assert ret['key'] == key
    assert ret['hash'] == etag(upload_file_name)
    os.rename(upload_file_name, upload_file_name+'.old')
    return domain+'/'+key

file_name = 'test.png'
while True:
    time.sleep(1)
    print 'check..................'
    status, output = commands.getstatusoutput(pngpaste+' '+file_name)
    if output.find('No image data found on the clipboard') > 0:
        continue
    if status == 0:
        if os.path.exists(file_name+'.old'):
            if image_similar(file_name+'.old', file_name) > 0:
                url = upload_file(file_name, None)
                os.system('echo "'+url+'"|/usr/bin/pbcopy')
        else:
            url = upload_file(file_name, None)
            os.system('echo "'+url+'"|/usr/bin/pbcopy')
