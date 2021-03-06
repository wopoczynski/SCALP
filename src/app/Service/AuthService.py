from src.app.Model.User import User
import bcrypt
from flask import session


class AuthService:

    def __init__(self):
        self.user = User()
        return

    def login(self, data):
        if self.isRegistered(data['username']):
            return self.validateUser(data)
        else:
            return 'Please register first'

    def isRegistered(self, username):
        if self.user.userExsists(username):
            return True
        else:
            return False

    def validateUser(self, data):
        if self.validatePassword(data['username'], data['password']):
            return "Success"
        else:
            return 'Wrong Password'

    def createUser(self, data):
        if self.user.userExsists(data['username']):
            return "Username taken!"
        else:
            password = self.encodePassword(data['password'])
            user = User()
            user.username = data['username']
            user.name = data['name']
            user.surname = data['surname']
            user.email = data['email']
            user.password = password
            user.create()
            return "Success"

    def encodePassword(self, password):
        password = password.encode()
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)
        return hashed.decode("utf-8")

    def validatePassword(self, username, password):
        password = password.encode()
        hashed = self.user.getUserPasswordHash(username).encode()
        if bcrypt.checkpw(password, hashed):
            return True
        else:
            return False

    def checkAdmin(self, username):
        if self.user.checkAdmin(username) == True:
            session['isAdmin'] = True
        else:
            session['isAdmin'] = False
