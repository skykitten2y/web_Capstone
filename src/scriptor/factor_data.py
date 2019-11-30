from src.common.database import Database


class factor_data(object):

    def __init__(self, a, b):  # set a default value for id to be none
        self.a = a
        self.b = b

    def save_to_mongo(self):
        Database.insert(collection='factors',
                        data=self.json())
        pass


    def json(self):  # create a json representation of the survey
        return {
            'a': self.a,
            'b': self.b,

        }
