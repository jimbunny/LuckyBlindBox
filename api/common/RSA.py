#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2021/6/1 下午3:50
# software: PyCharm

import base64
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA

rsa_private_key = ''
with open('config/RSAKey/private.pem', 'r') as f:
    rsa_private_key = f.read()

def getRSAtext(cipher_text):
    # 前端加密后的密文串
    # cipher_text = 'oKxL9flsI4HdJq22G5D5K4kWAs/Y8IJ8/IQobdHpXyM03aucPbZUmTmC+6LRfDNtT+LwzBxlpLo1nleUlYhMPSK1TGxIoCXa7wdTbEOwe7R4s6L/81ihhK6c2G2+fGDVnwU3qzn25IDOu/qgpUlRuo14xKgPD72COP/AfF4W5pI='
    rsakey = RSA.importKey(rsa_private_key)  # 导入私钥
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    random_generator = Random.new().read
    text = cipher.decrypt(base64.b64decode(cipher_text), None)
    # print(text.decode('utf8'))
    return text.decode('utf8')