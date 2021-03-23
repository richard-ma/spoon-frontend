from spoonfrontend.mail import Mail
from settings import *

if __name__ == '__main__':
    host = MAIL_HOST
    port = MAIL_PORT
    username = MAIL_USERNAME
    password = MAIL_PASSWORD
    receiver = username  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    subject = '测试标题'
    message = '测试内容'

    server = Mail(host, port, username, password, ssl=True)
    server.send(receiver, subject, message)