#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/v1/email', methods=['POST'])
def send_email():
    if request.method == 'POST':
        print("request data?{}".format(request.json))
        email_type = request.json.get('email_type')
        recipient_list = request.json.get('recipient_list')
        language_code = request.json.get('language_code', 'en')
        params = request.json.get('params')
        email_format = request.json.get('email_format', 'txt')
        print("email_type: {}, recipient_list: {}, language_code: {}, params: {}, email_format: {}".format(email_type, recipient_list, language_code, params, email_format))

        sender = 'zhihu2ebook@hotmail.com'    # 这里改成自己的邮箱
        msg = email.message_from_string('test')
        msg['From'] = sender
        msg['To'] = ','.join(recipient_list)
        msg['Subject'] = 'for test'
        server = None
        # try:
        server = smtplib.SMTP_SSL("smtp.live.com", 587)
        server.login('zhihu2ebook@hotmail.com', 'Zhihu2Ebook')
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.sendmail(sender, recipient_list, msg.as_string)
        print("WTF")
        # except Exception as e:
        print("Some thing happen")
        # finally:
        if server:
            server.quit()
        print("WTF is this???")
    return '', 204


if __name__ == "__main__":
    app.run()
