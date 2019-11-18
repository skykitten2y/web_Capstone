
from flask import session
from src.common.database import Database



class User(object):
    def __init__(self,email,password,_id=None):
        self.email = email
        self.password = password


    @classmethod  # A class method takes cls as first parameter while a static method needs no specific parameters
    def get_by_email(cls, email):
        data = Database.find_one("users", {"email": email})
        if data is not None:
            return cls(**data)


    @staticmethod
    def login_valid(email, password):
        # Check whether a user's email matches the password they sent us
        user = User.get_by_email(email)
        if user is not None:
            # Check the password
            return user.password == password
        return False

    @staticmethod
    def address_valid(email, password):
        # check if only address are correct, user input wrong email
        user = User.get_by_email(email)
        if user is None:
            return not user.password == password
        return True

    @staticmethod
    def duplicate_register(email):
        user = User.get_by_email(email)
        if user is not None:
            # check the password
            return True
        return False

    @classmethod
    def register(cls, email, password):
        user = cls.get_by_email(email)
        if user is None:
            # User doesn't exist, so we can create it
            new_user = cls(email, password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            # User exists :(
            return False

#cookie: a way to store information on the web browser. Session is another to save user's info
# Cookies are only stored on the client-side machine, while sessions get stored on the client as well as a server.
# and user send us an identifier with cookie, we use the identifier to get the associated information, and user email is passed by session
#(sercruity reason to prevent users modify cookies)
    @staticmethod
    def login(user_email):
    # login_valid has already been called
        session['email'] = user_email #only store user_email in the session when they login in
    #Flask handles users' cookies automatically


    @staticmethod
    def logout():
        session['email'] = None



    def json(self):
        return{
            "email": self.email,
            "password": self.password  #this is not safe to send over the network
        }

    def save_to_mongo(self):
        Database.insertOne("users", self.json())

    @staticmethod
    def find_risklevel( answer_q1, answer_q2, answer_q3,answer_q4,answer_q5,answer_q6,answer_q7,answer_q8):
        rw = 0  # risk_weight
        # q1
        if (answer_q1 == "Male"):
            rw = rw + 1
        else:
            rw = rw + 0
        # q2
        if (answer_q2 == "18-30"):
            rw = rw + 2
        elif (answer_q2 == "30-45"):
            rw = rw + 3
        elif (answer_q2 == "45-60"):
            rw = rw + 2
        elif(answer_q2 == "60+"):
            rw = rw + 1
        else:
            rw =rw + 0
        # q3
        if (answer_q3 == "Employed"):
            rw = rw + 3
        elif (answer_q3 == "Unemployed"):
            rw = rw + 2
        elif(answer_q3 == "Retired"):
            rw = rw + 1
        else:
            rw = rw +0
        # q4
        if (answer_q4 == "No"):
            rw = rw + 5
        elif (answer_q4 == "Within 1-3 years"):
            rw = rw + 1
        elif (answer_q4 == "Within 3-5 years"):
            rw = rw + 2
        elif( answer_q4 == "More than 5 years"):
            rw = rw + 3
        else:
            rw = rw+0
        # q5
        if (answer_q5 == "No"):
            rw = rw + 5
        elif (answer_q5 == "Within 1-3 years"):
            rw = rw + 1
        elif (answer_q5 == "Within 3-5 years"):
            rw = rw + 2
        elif (answer_q5 == "More than 5 years"):
            rw = rw + 3
        else:
            rw = rw + 0
        # q6
        if (answer_q6 == "No"):
            rw = rw + 5
        elif (answer_q6 == "Within 1-3 years"):
            rw = rw + 1
        elif (answer_q6 == "Within 3-5 years"):
            rw = rw + 2
        elif (answer_q6 == "More than 5 years"):
            rw = rw + 3
        else:
            rw = rw + 0
        # q7
        if (answer_q7 == "30k-50k"):
            rw = rw + 1
        elif (answer_q7 == "50k-100k"):
            rw = rw + 2
        elif (answer_q7 == "100k-200k"):
            rw = rw + 3
        elif(answer_q7 == "more than 200k"):
            rw = rw + 4
        else:
            rw = rw+0
        # q8
        if (answer_q8 == "Strongly Agree"):
            rw = rw + 1
        elif (answer_q8 == "Agree"):
            rw = rw + 2
        elif (answer_q8 == "Disagree"):
            rw = rw + 3
        elif(answer_q8 == "Strongly Disagree"):
            rw = rw + 4
        else:
            rw = rw+0
        return rw