from werkzeug.security import check_password_hash
class User:
    def __init__(self,username,password,mailid):
        self.username=username
        self.password=password
        self.mailid=mailid

    def is_authenticated(self):
        return True

    def is_active(self):
        return True             

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username         

    def check_password(self,password_input):
        return check_password_hash(self.password,password_input)