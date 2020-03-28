import requests as req

class API():
    host = ''
    SecretToken = ''

    def __init__(self, host, SecretToken):
        if req.get(host).status_code == 200:
            self.host = str(host)
            self.SecretToken = str(SecretToken)

            print('___________BAPI WORK!_______')
            print('Host: {0}, SecterToken: {1}'.format(host, SecretToken), end='\n\n')

    def IsUser(self, idUser):
        path = '/isuser?idtelegram={0}&SecretToken={1}'.format(idUser, self.SecretToken)
        response = req.get(self.host + path)
        
        if response.text == 'True' or response.text == 'False':
            return response.text
        return  'Error'

    def AddUser(self, idUser, Name, Surname, Phone):
        path = '/adduser?idtelegram={0}&SecretToken={1}&name={2}&surname={3}&mobilenumber={4}'.format(idUser, self.SecretToken, Name, Surname, Phone)
        response = req.get(self.host + path)

        if response.text == 'True':
            return True
        return False

    def AddNumber(self, idUser, Numbername, Carnumber):
        path = '/addnumber?idtelegram={0}&SecretToken={1}&numbername={2}&carnumber={3}'.format(idUser, self.SecretToken, Numbername, Carnumber)
        response = req.get(self.host + path)
        
        if response.text == 'True':
            return True
        return False

    def GetStatus(self, idUser):
        path = '/getstatus?idtelegram={0}&SecretToken={1}'.format(idUser, self.SecretToken)
        response = req.get(self.host + path)
        
        if response.text != 'Errors' and response.text != 'Errors in get parameters' and response.text != 'Parks is not':
            return response.text
        return False
    


a = API('http://sergey223344.pythonanywhere.com', '1234')

print(a.GetStatus('777'))