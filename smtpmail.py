import smtplib
import json
from threading import Thread
from threading import Lock



class mailsender:
    smtp_server = ''
    smtp_port = 0
    smtp_enc = False
    auth = False
    auth_login = ''
    auth_password = ''
    confName = 'smtpconf'
    mutex = Lock()
    #confmutex = Lock()

    def __init__(self):
        self.__parseconfig(mailsender.confName)
        self.__initself()

    def __initself(self):
        self.__smtpObj = None
        self.__thread = None
        self.__smtp_server = mailsender.smtp_server
        self.__smtp_port = mailsender.smtp_port
        self.__smtp_enc = mailsender.smtp_enc
        self.__auth = mailsender.auth
        self.__auth_login = mailsender.auth_login
        self.__auth_password = mailsender.auth_password

    def __startsmtp(self):
        #start new connection
        if self.__smtpObj:
            self.__smtpObj.quit()

        self.__smtpObj = smtplib.SMTP(mailsender.smtp_server, mailsender.smtp_port)
        if self.__smtpObj:
            if self.__smtp_enc:
                try:
                    self.__smtpObj.starttls()
                except Exception as ex:
                    print("Can't start encryption : " + str(ex))
                    self.__smtpObj.quit()
                    self.__smtpObj = None

            if self.__auth:
                try:
                    self.__smtpObj.login(self.__auth_login, self.__auth_password)
                except:
                    print("Can't login to smtp server")
                    self.__smtpObj.quit()
                    self.__smtpObj = None

    def __mailsend(self, fromaddr, toaddr, text, subject, signature):
        mailsender.mutex.acquire()

        self.__startsmtp()

        if self.__smtpObj:
            text = 'Subject: {}\n\n{}'.format(subject, text)

            if fromaddr:
                text = 'From: {} <{}>\n{}'.format(fromaddr, fromaddr, text)

            text = 'To: {} <{}>\n{}'.format(toaddr, toaddr, text)
            text = text + "\n\n" + signature + "\n"
            self.__smtpObj.sendmail(fromaddr, toaddr, text)

        mailsender.mutex.release()

    def __parseconfig(self, file):
        #mailsender.confmutex.acquire()
        mailsender.mutex.acquire()

        #json config parse
        try:
            with open(file) as json_file:
                data = json.load(json_file)
                
                self.__smtp_server = data['smtp_server_address']
                self.__smtp_port = data['smtp_server_port']
                self.__smtp_enc = bool(int(data['smtp_server_encryption_enabled']))
                self.__auth = bool(int(data['smtp_server_authentication_enabled']))
                self.__auth_login = data['smtp_server_authentication_login']
                self.__auth_password = data['smtp_server_authentication_password']

                mailsender.smtp_server = data['smtp_server_address']
                mailsender.smtp_port = data['smtp_server_port']
                mailsender.smtp_enc = bool(int(data['smtp_server_encryption_enabled']))
                mailsender.auth = bool(int(data['smtp_server_authentication_enabled']))
                mailsender.auth_login = data['smtp_server_authentication_login']
                mailsender.auth_password = data['smtp_server_authentication_password']
        except Exception as ex:
            print(str(ex))

        mailsender.mutex.release()

        #mailsender.confmutex.release()

    def setconf(confFile):
        self.__parseconfig(confFile)
        self.__initself()

    def sendmessage(self, fromaddr, toaddr, text, subject, signature):
        #reparse config
        self.__parseconfig(mailsender.confName)
        #send mail
        self.thread = Thread(target=self.__mailsend, args=(fromaddr, toaddr, text, subject, signature))
        self.thread.start()
        #self.__mailsend(fromaddr, toaddr, text, subject, signature)

    def printself(self):
        print("smtp_server = " + self.__smtp_server)
        print("smtp_port = " + str(self.__smtp_port))
        print("smtp_enc = " + str(self.__smtp_enc))
        print("auth = " + str(self.__auth))
        print("auth_login = " + self.__auth_login)
        print("auth_password = " + self.__auth_password)
        print("")

    def __del__(self):
        if self.__smtpObj:
            self.__smtpObj.quit()
