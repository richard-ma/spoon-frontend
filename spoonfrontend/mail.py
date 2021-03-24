import smtplib
from email.mime.text import MIMEText
from email.header import Header


class Mail():
    @staticmethod
    def _connection(host, port, ssl):
        try:
            if ssl is True:
                conn = smtplib.SMTP_SSL(host=host, port=port)
            else:
                conn = smtplib.SMTP(host=host, port=port)
            return conn
        except smtplib.SMTPException as e:
            raise e

    @staticmethod
    def _login(connection, username, password):
        connection.login(username, password)

    def __init__(self,
                 host,
                 port=0,
                 username=None,
                 password=None,
                 ssl=False,
                 sender=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ssl = ssl

        if sender is not None:
            self.sender = sender
        else:
            self.sender = username

        self.conn = Mail._connection(self.host, self.port, self.ssl)

        if username is not None:
            Mail._login(self.conn, username, password)

    def send(self,
             receiver,
             subject,
             message,
             message_type='plain',
             encoding='utf-8'):
        # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
        information = MIMEText(message, message_type, encoding)
        information['From'] = Header(self.sender, encoding)  # 发送者
        information['To'] = Header(receiver, encoding)  # 接收者
        information['Subject'] = Header(subject, encoding)  # 标题
        try:
            self.conn.sendmail(self.sender, receiver, information.as_string())
        except smtplib.SMTPException as e:
            raise e
