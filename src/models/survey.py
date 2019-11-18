

from src.common.database import Database


class Survey(object):
    # need to get num_assets, inv_time, reb_time, risk_measure,return_goal (starting from answer_q_13, the info before is only for storage purpose)

    def __init__(self, email, gender, age, employment, house, car, education,income, protect, name,num_asset,inv_time,
                 reb_time, risk_measure, ret_goal=None, given_portfolio=None, _id=None):  # set a default value for id to be none
        self.email = email
        self.gender = gender
        self.age = age
        self.employment = employment
        self.house = house
        self.car = car
        self.education = education
        self.income = income
        self.protect = protect
        self.name = name
        self.num_asset = num_asset
        self.inv_time = inv_time
        self. reb_time = reb_time
        self.risk_measure = risk_measure
        self.ret_goal = ret_goal
        self. given_portfolio = given_portfolio



    # def new_survey(self,  email, gender, age, employment, house, car, education,income, protect, name, phone, citizenship,num_assets,inv_time,
    #              reb_time, risk_measure, ret_goal, inp_portfolio):
    #     survey = Survey()
    #     survey.save_to_mongo()


    def save_to_mongo(self):
        Database.insert(collection='surveys',
                        data=self.json())
        pass



    @classmethod

    def get_by_email(cls,email):
        return [survey for survey in Database.find(collection = 'surveys',query = {'email':email})]


    def check_by_email(email):
        data = Database.find_one(collection = 'surveys',query = {'email':email})
        if data is not None:
            return data



    @staticmethod
    def survey_not_empty(email):
        survey = Survey.check_by_email(email)
        if survey is not None:
            # check the password
            return True
        return False

    def json(self):  # create a json representation of the survey
        return {
            'email': self.email,
            'gender': self.gender,
            'age': self.age,
            'employment': self.employment,
            'house': self.house,
            'car': self.car,
            'education':self.education,
            'income':self.income,
            'protect':self.protect,
            'name':self.name,
            'num_asset':self.num_asset,
            'inv_time':self.inv_time,
            'reb_time':self.reb_time,
            'risk_measure':self.risk_measure,
            'ret_goal':self.ret_goal,
            'given_portfolio':self.given_portfolio

        }
