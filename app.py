from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)

app.config['SECRET_KEY'] = 'fruitsmell8754'
debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def home_page():
    """Shows home page with list of surveys to choose from"""
    return render_template('home.html',
                            surveys=surveys)

@app.route('/survey_chosen')
def route_to_chosen_survey():
    """Collects the user's selection as a variable, chosen_survey, and redirects to that survey's page"""
    chosen_survey = request.args['survey']
    return redirect(f"/survey/{chosen_survey}")

@app.route('/survey/<chosen_survey>')
def survey_page(chosen_survey):
    """Shows chosen_survey instructions and start button"""
    try:
        if len(session[chosen_survey]) >= len(surveys[chosen_survey].questions):
            flash("Warning: you have already completed this survey. Pressing start will erase all of your previous responses.", 'error')
    finally:
        return render_template('survey.html',
                                surveys=surveys,
                                chosen_survey=chosen_survey)

@app.route('/survey/<chosen_survey>/session_init', methods=["POST"])
def session_init(chosen_survey):
    """Initializes an object in session"""
    session[chosen_survey] = []
    return redirect(f"/survey/{chosen_survey}/questions/0")

@app.route('/survey/<chosen_survey>/questions/<int:question_number>')
def question_page(chosen_survey, question_number):
    """Shows question by chosen_survey and question_number"""
    num_of_answers = len(session[chosen_survey])
    if num_of_answers >= len(surveys[chosen_survey].questions):
        return redirect(f"/survey/{chosen_survey}/thank_you")
    elif num_of_answers != question_number:
        flash("Questions must be answered in order.", 'error')
        return redirect(f"/survey/{chosen_survey}/questions/{num_of_answers}")
    return render_template('question.html',
                            chosen_survey=chosen_survey,
                            question_number=question_number,
                            surveys=surveys)

@app.route('/survey/<chosen_survey>/questions/<int:question_number>/answer', methods=["POST"])
def record_answer(chosen_survey, question_number):
    """Records the answer provided by the user in a list"""
    answer = request.form["answer"]
    survey_answers = session[chosen_survey]
    survey_answers.append(answer)
    session[chosen_survey] = survey_answers
    question_number += 1
    return redirect(f"/survey/{chosen_survey}/questions/{question_number}") 

@app.route('/survey/<chosen_survey>/thank_you')
def show_thank_you(chosen_survey):
    """Shows the thank you page after completing survey"""
    return render_template('thank_you.html',
                            chosen_survey=chosen_survey,
                            surveys=surveys)