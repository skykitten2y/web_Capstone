from src.common.database import Database
from src.models.survey import Survey


class Menu(object):
    def __init__(self):
        # Ask user for account name Q: what happen for repeated names?
        # Check if they've already got an account
        # If not, prompt them to create one
        self.user_name = input("Enter your user name: ")
        self.user_password = input("Enter your user password: ")
        if self._user_has_account():  #convention: underscore indicates private method, only call it in the class
            print("Welcome back {}".format(self.user_name))
        else:
            self._prompt_user_for_account()

    def _user_has_account(self):
        Database.find_one('surveys', {'name':self.user_name, 'password':self.user_password}) is not None

    def _prompt_user_for_account(self):
        name = input("Enter your user name: ")
        password = input("Enter your password: ")
        age = input("Enter your age: ")
        gender = input("Enter your gender: ")
        incomelevel = input("Enter your income level: " )
        risklevel = input("Engter your risk level: ")

        survey = Survey(name,password,age,gender,incomelevel,risklevel)
        survey.save_to_mongo()

    def run_menu(self):
        #User start finding the portfolio? (click a button "start")
        start = input("Do you want to start? Yes(Y) or No(N)")
        if start == 'Y':
            #start optimization model and display results
            pass
        else:
            print("Bye")



