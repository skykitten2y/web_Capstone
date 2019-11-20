
from flask import Flask, render_template, request, session
from src.common.database import Database
from src.models.user import User
from src.models.survey import Survey





app = Flask(__name__) #'  main  '

app.secret_key ="Leon19970309" #flask uses to make sure cookie is secure

@app.route('/')
def home_template():
    return render_template('home.html')


@app.route('/login')  #127.0.0.1:5000/login  define route
def login_template(): # defined the method, access the end point
    return render_template('login.html')

@app.route('/register')  #127.0.0.1:5000/register
def register_template():
    return render_template('register.html')

@app.before_first_request
def initialize_database():
    Database.initialize()

@app.route('/auth/login', methods=['POST'])   #define a new end point to login user, get the email and passwords and log user in
def login_user():
    email = request.form['email'] #website is going to make a request to form from login.htmal for email and password (from Id)
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
        return render_template("choose_extract.html")  # give a render_template with data you want, by variable email.
    else:
        return render_template('login_wrong_password.html')



@app.route('/auth/register', methods =['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']
    if User.duplicate_register(email):
        return render_template('register_duplicate_address.html')
    else:
        User.register(email, password)
        return render_template("choose_function.html", email=session['email'])

@app.route('/extract_existing_info', methods = ['POST'])
def extract_existing():
    answer_q17 = request.form.get('q17')
    if(answer_q17 == 'Yes'):
        if Survey.survey_not_empty(session.get('email',None)):
            existing_survey = Survey.get_by_email(session.get('email', None))
            answer_q9 = existing_survey[0].get('name')
            answer_q13 = existing_survey[0].get('num_asset')
            answer_q14 = existing_survey[0].get('inv_time')
            answer_q15 = existing_survey[0].get('reb_time')
            answer_q1 = existing_survey[0].get('age')
            answer_q2 = existing_survey[0].get('gender')
            answer_q3 = existing_survey[0].get('employment')
            answer_q4 = existing_survey[0].get('house')
            answer_q5 = existing_survey[0].get('car')
            answer_q6 = existing_survey[0].get('education')
            answer_q7 = existing_survey[0].get('income')
            answer_q8 = existing_survey[0].get('protect')
            return render_template("existing_results.html", existing_survey = existing_survey,
                                   answer_q9 = answer_q9,answer_q13 = answer_q13,answer_q14 = answer_q14,answer_q15 = answer_q15,answer_q1 = answer_q1,
                                   answer_q2 = answer_q2,answer_q3 = answer_q3,answer_q4 = answer_q4,answer_q5 = answer_q5,answer_q6 = answer_q6,
                                   answer_q7 = answer_q7,answer_q8 = answer_q8)

        else:
            return render_template("force_input_survey.html")

    else:
        return render_template("choose_function.html")

@app.route('/directed_choose_function',methods =['POST'])
def directed_choose_function():
    return render_template("choose_function.html")


@app.route('/existing_choose_function', methods= ['POST'])
def existing_choose_function():
    return render_template("existing_choose_function.html")



@app.route('/choose_function',methods = ['POST'])
def choose_function():
    answer_q16 = request.form.get('q16')
    session['answer_q16'] = request.form.get('q16')
    return render_template("survey.html", answer_q16 = answer_q16)

@app.route('/survey/confirm', methods =['POST'])
def confirm_survey():
    answer_q9 = request.form.get('name')
    answer_q13 = request.form.get('assets')
    answer_q14 = request.form.get('horizon')
    answer_q15 = request.form.get('rebalance')
    answer_q1 = request.form.get('q1')
    answer_q2 = request.form.get('q2')
    answer_q3 = request.form.get('q3')
    answer_q4 = request.form.get('q4')
    answer_q5 = request.form.get('q5')
    answer_q6 = request.form.get('q6')
    answer_q7 = request.form.get('q7')
    answer_q8 = request.form.get('q8')

# delete q10, q11


    rw = User.find_risklevel(answer_q1, answer_q2, answer_q3,answer_q4,answer_q5,answer_q6,answer_q7, answer_q8)

    #Save to database, using survey Object

    new_survey = Survey(session.get('email',None), answer_q1,answer_q2,answer_q3,answer_q4,answer_q5,answer_q6,answer_q7,
                        answer_q8,answer_q9, answer_q13, answer_q14,answer_q15, rw)

    #need to get num_assets, inv_time, reb_time, risk_measure,return goal (starting from answer_q_13, the userf info beforehand is only for storage purpose)
    Survey.save_to_mongo(new_survey)

    return render_template("survey_results.html", answer_q1=answer_q1, answer_q2=answer_q2, answer_q3=answer_q3,
                           answer_q4=answer_q4, answer_q5=answer_q5, answer_q6=answer_q6, answer_q7=answer_q7,
                           answer_q8=answer_q8, answer_q9=answer_q9
                           , answer_q13 = answer_q13, answer_q14 =answer_q14, answer_q15=answer_q15,  rw = rw)


@app.route('/portfolio', methods=['POST'])
def portfolio_options():
    if (session.get('answer_q16', None) == "Get the risk and return profile for given portfolio"):
        return render_template("given_portfolio_ask.html")
    elif (session.get('answer_q16', None) == "Get the optimal portfolio without return"):
        return render_template("portfolio_without_return.html")
    elif (session.get('answer_q16', None) == "Get the optimal portfolio with return"):
        return render_template("portfolio_with_return_ask.html")
    else:
        pass

@app.route('/existing_portfolio',methods = ['POST'])
def existing_portfolio_options():
    e_answer_q16 = request.form.get('e_q16')
    if (e_answer_q16 == "Get the risk and return profile for given portfolio"):
        return render_template("given_portfolio_ask.html") #given_portfolio_ask.thml
    elif (e_answer_q16 == "Get the optimal portfolio without return"):
        return render_template("portfolio_without_return.html")
    elif (e_answer_q16 == "Get the optimal portfolio with return"):
        return render_template("portfolio_with_return_ask.html")
    else:
        pass



@app.route('/portfoilo/with_return',methods=['POST'])
def store_investor_expected_return():
    updated_survey = Database.find_one("surveys", {"email":session.get('email',None)})
    updated_survey["ret_goal"]= request.form.get('goal') #change 10 to user inputed return goal
    Database.replace_data('surveys',{"email":session.get('email',None)}, updated_survey)
    return render_template("portfolio_with_return_results.html")

@app.route('/portfoilo/input_portfolio',methods=['POST'])
def investor_input_portfolio():
    updated_survey = Database.find_one("surveys", {"email": session.get('email', None)})
    updated_survey["inp_portfolio"] = request.form.get('input')  # change 10 to user inputed return goal
    Database.replace_data('surveys', {"email": session.get('email', None)}, updated_survey)
    return render_template("portfolio_without_return_results.html")


@app.route('/portfolio/confirm_inputed_portfolio',methods=['POST'])
def confirm_input_portfolio():
    input_portfolio = request.form.getlist('input_portfolio')
    return render_template("given_portfolio_results.html", input_portfolio = input_portfolio)
@app.route('/')
# @app.route('/portfolio/results', methods = ['POST]'])
def results():
    stock = ['AAPL','MSFT','GOOG','GOOGL','AMZN']
    weight = [0.5,0.2,0.1,0,0.1]


    return render_template("charts_demo.html",weight = weight, stock = stock)

if __name__ == '__main__': #execute

    app.run(port=5000, debug=True) # need this to update





