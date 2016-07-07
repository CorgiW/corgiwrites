
from flask import (
    abort
    Flask,
    flash,
    g,
    session,
    redirect,
    render_template,
    request,
)
from flask.ext.mongoengine import MongoEngine

import datetime
import hashlib
import os
import random


app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': 'corgiwrites'}
app.config["SECRET_KEY"] = os.urandom(12)
app.config["DEBUG"] = True

db = MongoEngine(app)

import models

@app.route('/')
def front():
    if user not logged_in:
        return """Welcome to Corgiwrites, your source for corgis and writing."""
    else:
        # redirect to the dashboard

@app.route('/login', methods=['GET', 'POST'])
def login():
    #This is meant to redirect an already logged in user to the dashboard if they go onto this page. Not sure if right though
    if session['is_logged_in'] = True
        flash.message = "You are already logged in"
        return redirect('/dashboard')

    if request.method == 'GET':
        # display the login form

    else:
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        if username is not None and password is not None:
            # look up in the database if the password matches for the username
            user = models.User.objects.get(username=username)
            if user is None:
                # display an error and the login form
                flash.message = "User doesn't exist"
                return redirect('/login')
            if user.password == hashlib.sha256(password).hexdigest():
                # log the user in
                session['is_logged_in'] = True
                session['username'] = username
                return redirect('/dashboard')
            else:
                # display an error and the login form
                flash.message = "Wrong password"
                return redirect('/login')
        else:
            # display the login form
            flash.message = 'Both username and password are required'
            return redirect('/login')

@app.route('/logout')
def logout():
    # log the user out
    session['is_logged_in'] = False
    session['username'] = None
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        # display the register form
    else:
        username = request.form.get('username', None)
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        password_confirm = request.form.get('password_confirm', None)
        if username is None or email is None or password is None:
            flash.message = "All fields are required"
            return redirect('/register')
        if password != password_confirm:
            flash.message = "Please enter your password correctly both times"
            return redirect('/register')
        user_exists = models.User.objects.get(username=username)
        if user_exists is None:
            # start the registration process
            # create a user in the database with the provided username and password and email
            user = models.User()
            user.username = username
            user.email = email
            user.password = hashlib.sha256(password).hexdigest()
            # save the user
            user.save()
            # send them to the login screen
            return redirect('/login')
        else:
            # Warn the user that the username is taken and start over
            flash.message = "That username already exists in the database!"
            return redirect('/register')

@app.route('/story/create', methods=['GET', 'POST'])
def create_story():
    if not session['is_logged_in']:
        return redirect('/login')
    user = models.User.objects.get(username=session['username'])
    if request.method == 'GET':
        # show them the story creation form
    else:
        # save the information to the database
        title = request.form.get('title', None)
        if title is None:
            flash.message = "Title is required"
            return redirect('/story/create')
        story = models.Story()
        story.title = title
        story.genre = request.form.get('genre', None)
        story.summary = request.form.get('summary', None)
        story.status = request.form.get('status', None)
        wordcount_text = request.form.get('wordcount', None)
        if wordcount_text is not None:
            wc_entry = models.WordCountEntry()
            wc_entry.wordcount = int(wordcount_text)
            story.wordcounts.append(wc_entry)
        story.save()
        user.stories.append(story)
        user.save()
        # send the user to the story page
        return redirect('/story/%s' % story.id)

@app.route('/story/view/<story_id>')
def view_story(story_id):
    if not session['is_logged_in']:
        return redirect('/login')
    story = models.Story.objects.get(id=story_id)
    if story is None:
        # TODO corgiw - find out how to show the user a 404 page
        # return a 404

        #Will need to finish the templates I think
        abort(404)
    if story.owner.username is not session['username']:
        # return a 404
        abort(404)
    # show the user the story

# First thing to do, make this route only take POST requests
@app.route('/story/wordcount/update')
def update_story_wordcount():
    if user not logged_in:
        # redirect to the login page
        return.redirect('\login')
    # fetch two things from the form:
        #   the story id
        story_update = request.form.get('story', None)
        #   the next wordcount
        new_wc = request.form.get('story', None)
    # both are required, make sure they're not None, throw an error if so
    if story_update = None, or new_wc = None:
        flash.message = "The story and the new wordcount are required"
    # fetch the story from the database using the story id
    story = models.object.Story.get(id=story_update)
    # create a new wordcount object
    wc = models.WordCountEntry()
    # set the wordcount on that object
    #TODO Make it so that if the user enters in text instead of a number, the programme can handle that
    wc.wordcount = int(new_wc)
    # append the object to the story's wordcount list
    story.wordcounts.append(wc)
    # save the story
    story.save()
    # redirect to the story's page
    return redircet('\story\<story_id>')


@app.route('/market/create', methods=['GET', 'POST'])
def create_market():
    if not session['is_logged_in']:
        return redirect('/login')
    if request.method == 'GET':
        # show them the market creation form
    else:
        market_name = request.form.get('name', None)
        if market_name is None:
            flash.message = "Market name is required"
            return redirect('/market/create')
        market = models.Market()
        market.name = market_name
        market.url = request.form.get('url', None)
        market.genre = request.form.get('genre', None)
        market.wordcount = int(request.form.get('wordcount', 0))
        # set the expiry date
        year = int(request.form.get('year', 0))
        month = int(request.form.get('month', 0))
        day = int(request.form.get('day', 0))
        if year > 0 and month > 0 and day > 0:
            market.expires = datetime.date(year, month, day)
        # save the information to the database
        market.save()
        # Send the user to the market ID
        # TODO corgiw use the proper market ID here
        return redirect('/market/<market_id>')

@app.route('/market/view/<market_id>')
def view_market(market_id):
    market = models.Market.objects.get(id=market_id)
    if market is None:
        # show the user a 404 page
        return None
    today = datetime.date.today()
    diff = today - market.expires
    if diff > 0:
        market.is_active = False
        market.save()
    # show the user the page for the market

@app.route('/story/submit', methods=['POST'])
def submit_story():
    if not session['is_logged_in']:
        return redirect('/login')
    user = methods.User.objects.get(username=session['username'])
    story_id = request.forms.get('story_id', None)
    market_id = request.forms.get('market_id', None)
    if story_id is None:
        flash.message = "Something went wrong and we didn't receive the data we were expecting!"
        return redirect('/dashboard')
    if market_id is None:
        flash.message = "Market id is required"
        # TODO corgiw use the proper story ID
        return redirect('/story/fakestoryid')
    story = None
    for s in user.stories:
        if s.id == story_id:
            story = s
    if story is None:
        flash.message = "That story wasn't found"
        return redirect('/dashboard')
    market = models.Market.objects.get(id=market_id)
    if market is not None:
        # add the story to the market by creating a submission in the database, with the status of 'waiting' and the current date
        submission = models.Submission()
        submission.market = market
        submission.status = 'waiting'
        story.submissions.append(submission)
        user.save()
        # redirect to the story page
        return redirect('/story/fakestoryid')
    else
        flash.message = "We couldn't find that market!"
    # TODO corgiw use the proper story ID here
        return redirect('/story/<story_id')


@app.route('/submission/<submission_id>', methods=['POST'])
def update_submission(submission_id):
    if not session['is_logged_in']:
        # redirect to the login page
        return redircet('/login')
    # get the submission from the database
    submission_exists = models.Submission.objects.get(id=submission_id)
    if submission_exists is None:
        abort(404)
    # change the submission status
    else:
        submission = models.Submission
        new_status = request.form.get('status', None)
        submission.status = new_status
    # save the submission back to the database
        submission.save()
    # redirect to the story page
        flash.message = "Story submission has been updated"
        return.redirect("/story/view")

@app.route('/dashboard')
def dashboard():
    if user not logged_in:
        # redirect to the login page
        return
    # get the current user
    # get the wordcounts by day
    # get the list of stories and submission statuses
    # display a page with all of this information
'''
Actions to do:
* login
* logout
* register
* add story
* update wordcount
* submit story to market
* update submission
* add market
* update market
* dashboard
    * list of stories with statuses
    * daily wordcount
* view story
* view market
'''

if __name__ == '__main__':
    app.run()
