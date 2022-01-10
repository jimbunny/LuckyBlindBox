#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2021/5/31 下午2:22
# software: PyCharm

from flask_mail import Message
import yagmail
from flask import current_app


def send_email(to, subject, template):
    yagmail.SMTP(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD']).send(to, subject, template)
    # msg = Message(
    #     subject,
    #     recipients=[to],
    #     html=template,
    #     sender=current_app.config['MAIL_DEFAULT_SENDER']
    # )
    # mail.send(msg)
    # wozhdpvhetjtbpjr