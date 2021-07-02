from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from flask_qa.extensions import db
from flask_qa.models import Question, User

main = Blueprint("main", __name__)

@main.route("/")
def index():
    questions = Question.query.filter(Question.answer != None).all()
    return render_template("home.html", questions=questions)

@main.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    if request.method == 'POST':
        question = request.form['question']
        expert = request.form['expert']

        question = Question(
            question=question, 
            expert_id=expert, 
            asked_by_id=current_user.id
        )

        db.session.add(question)
        db.session.commit()

        return redirect(url_for('main.index'))

    experts = User.query.filter_by(expert=True).all()

    context = {
        'experts' : experts
    }

    return render_template('ask.html',**context, current_user=current_user)

@main.route('/question/<int:question_id>')
def question(question_id):
    question = Question.query.get_or_404(question_id)


    context = {
        'question' : question
    }

    return render_template('question.html', **context, current_user=current_user)




@main.route('/unanswered')
@login_required
def unanswered():
    if not current_user.expert:
        return redirect(url_for('main.index'))

    unanswered_questions = Question.query\
        .filter_by(expert_id=current_user.id)\
        .filter(Question.answer == None)\
        .all()

    context = {
        'unanswered_questions' : unanswered_questions
    }

    return render_template('unanswered.html', **context)

@main.route('/un_answered/<int:question_id>')
@login_required
def un_answered(question_id):
    question = Question.query.get_or_404(question_id)


    context = {
        'question' : question
    }
    

    return render_template("unanswered_question.html", **context, current_user=current_user)

@main.route("/users")
def users():
    users = User.query.all()


    return render_template('users.html', users=users)


@main.route('/answer/<int:question_id>', methods=['GET', 'POST'])
@login_required
def answer(question_id):
    if not current_user.expert:
        return redirect(url_for('main.index'))

    question = Question.query.get_or_404(question_id)

    if request.method == 'POST':
        question.answer = request.form['answer']
        
        db.session.commit()

        return redirect(url_for('main.unanswered'))

    context = {
        'question' : question
    }

    return render_template('answer.html', **context)

@main.route('/promote/<int:user_id>')
@login_required
def promote(user_id):
    if not current_user.admin:
        return redirect(url_for('main.index'))

    user = User.query.get_or_404(user_id)
    if user.expert:
        user.expert == False

    user.expert = True 
    db.session.commit()

    return redirect(url_for('main.users'))

@main.route('/depromote/<int:user_id>')
@login_required
def depromote(user_id):
    if not current_user.admin:
        return redirect(url_for('main.index'))

    user = User.query.get_or_404(user_id)

    user.expert = False 
    db.session.commit()

    return redirect(url_for('main.users'))

@main.route("/delete_question/<int:question_id>")
@login_required
def delete_question(question_id):
    
    asker = Question.query.filter_by(id=question_id).first()
    if current_user.id ==  asker.asker.id or current_user.admin:
        db.session.delete(asker)
        db.session.commit()
        
        return redirect(url_for("main.index"))


    return redirect(url_for("main.index"))


    

@main.route("/user_questions")
@login_required
def user_questions():
    questions = Question.query.filter_by(asked_by_id=current_user.id).filter(Question.answer == None).all()

    return render_template("user_unanswered_questions.html", questions=questions)

@main.route("/profile")
@login_required
def profile():
    user = User.query.filter_by(id=current_user.id).first()


    return render_template("profile.html", user=user)

@main.route("/delete_user")
@login_required
def delete_user():
    user = User.query.filter_by(id=current_user.id).delete()
    db.session.commit()

    return redirect(url_for("main.index"))