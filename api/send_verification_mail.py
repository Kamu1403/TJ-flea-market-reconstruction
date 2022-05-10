from email.mime.message import MIMEMessage
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.image import MIMEImage
import logging
import asyncio


def forma(s: str) -> str:
    return s.replace('\\', '/').replace('//', '/').split('/')[-1]


async def emailChanel(sender, receiverList, user, emailPwd, smtpServer, commonPort, emailTitle, htmlPath=None, attachPathList=None, text=None):
    try:
        multiPart = MIMEMultipart()
        multiPart['From'] = sender
        multiPart['To'] = ','.join(receiverList)
        subject = emailTitle
        multiPart['Subject'] = Header(subject, "utf-8")

        if text == None and htmlPath == None:
            raise RuntimeError("邮件格式错误：没有传入正文！")

        # 正文/html
        if htmlPath != None:
            if os.path.isfile(htmlPath):
                if os.path.exists(htmlPath):
                    pass
                else:
                    raise IOError("htmlPath not exist")
            else:
                raise IOError("html path is not file..")
            emailBody = MIMEText(_text=open(htmlPath, 'rb').read(), _subtype='html', _charset="utf-8")
            multiPart.attach(emailBody)
        # 正文/text
        elif text != None:
            if isinstance(text, str):
                multiPart.attach(MIMEText(text, 'plain', 'utf-8'))
            else:
                raise TypeError(f"expected type is str,but get {type(text).__name__}")

        # 附件
        if attachPathList != None:
            if isinstance(attachPathList, list):
                for attachPath in attachPathList:
                    if os.path.exists(attachPath):
                        pass
                    else:
                        raise IOError("attachPath not exist")
            else:
                raise TypeError("expected type is list,but get {}".format(type(attachPathList).__name__))
            for attachPath in attachPathList:
                if os.path.splitext(attachPath)[-1] in [".png", ".jpg", ".webp", ".jpeg"]:
                    msg = MIMEImage(open(attachPath, 'rb').read(), _subtype='octet-stream')
                    msg.add_header('Content-Disposition', 'attachment', filename=forma(attachPath))
                    multiPart.attach(msg)
                else:
                    #if os.path.splitext(attachPath)[-1] == ".log":
                    # 第二种写法
                    msg = MIMEText(open(attachPath, 'rb').read(), 'base64', 'utf-8')
                    msg["Content-Type"] = 'application/octet-stream'
                    msg["Content-Disposition"] = f'attachment; filename={forma(attachPath)}'
                    multiPart.attach(msg)
        smtp = smtplib.SMTP(smtpServer, commonPort)
        try:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(user, emailPwd)
            smtp.sendmail(sender, receiverList, multiPart.as_string())
        except smtplib.SMTPException as e:
            raise RuntimeError(f"邮件发送失败: {e}")
        finally:  # 无论是否异常都执行的代码
            try:
                smtp.quit()
            except smtplib.SMTPException:
                logging.warning("smtp quit fail")
            return {"status": True, "message": "邮件发送成功"}
    except Exception as e:
        logging.error(e)
        return {"status": False, "message": repr(e)}


async def send_email(emailTitle: str, receiverList: list, text: str = None, htmlPath: str = None, attachPathList: list = None) -> json:
    if type(receiverList) == str:
        receiverList = [receiverList]
    sender = 'TongjiMarket@ellye.cn'
    user = 'TongjiMarket@ellye.cn'
    emailPwd = 'sn5diPhone6'
    smtpServer = 'smtp.office365.com'
    commonPort = 587
    return await emailChanel(sender, receiverList, user, emailPwd, smtpServer, commonPort, emailTitle, htmlPath, attachPathList, text)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    a = send_email("mail test", 'ellyeChen@tongji.edu.cn', "final13579")
    b = send_email("mail test", 'didiking@yeah.net', "final02468")
    print(loop.run_until_complete(asyncio.gather(a, b)))
    send_email()