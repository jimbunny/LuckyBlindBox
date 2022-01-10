#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2021/6/1 下午3:58
# software: PyCharm


from Crypto import Random
from Crypto.PublicKey import RSA

random_generator = Random.new().read
rsa = RSA.generate(1024, random_generator)

# 生成私钥
private_key = rsa.exportKey()
with open('private.pem', 'w') as f:
    f.write(private_key.decode('utf-8'))

# 生成公钥
public_key = rsa.publickey().exportKey()
with open('public.pem', 'w') as f:
    f.write(public_key.decode('utf-8'))