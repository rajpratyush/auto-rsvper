"""Contains user-defined Exception Class"""


class AuthorizationException(BaseException):
    #Raised when Meetup.com detects us and activates reCaptcha

    def __init__(self):
        print("Looks like our bot is detected.\nKindly use the browser to log in, until the reCaptcha is lifted")


class IncorrectInfoException(BaseException):
    #Raised when the wrong user information(userid and password) are entered

    def __init__(self):
        print("Your userid or password is incorrent.\nKindly recheck and enter the correct credentials")
