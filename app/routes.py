from flask import render_template, flash, redirect, url_for
from flask import current_app as app
from app import db
from app.form import LoginForm
from app.form import RegistrationForm
from app.form import CreateForm
from app.form import SearchForm
from app.models import User, Event
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from array import array
from datetime import datetime
from datetime import date






@app.route('/home')
@app.route('/')
def home():  
    return render_template('home.html', title='home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('userpage', username=current_user.username))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('userpage', username=current_user.username))
    return render_template('login.html', title='Sign in', form=form)
    
    
@app.route('/userpage/<username>')
@login_required
def userpage(username):
    user=User.query.filter_by(username=username).first_or_404()
    e= Event.query.order_by('event_date', 'event_timeStart').filter(Event.user_id == user.id,  Event.event_name!='vacancy').all()
    
    eventarray = []
    for i in e:
        eventarray.append(i)
    
    if (len(eventarray) == 0):
        return redirect(url_for('home'))
    
    currentday = date.today()
    c = currentday.strftime('%m/%d/%Y')

    for ee in eventarray:
        if (ee.event_date.strftime('%m/%d/%Y') == c):
            flash('You have an event today: ' + ee.event_name)
           
    return render_template('json.html',user=user, title= 'Profile',e=e)


    
    
    
@app.route('/delete/<i>', methods=['GET', 'POST'])
@login_required
def delete(i):
    Event_to_delete=  Event.query.get_or_404(i)
    
    try: 
        db.session.delete(Event_to_delete)
        db.session.commit()
        return redirect(url_for('userpage',username=current_user.username))
        
    except:
        return "there is a problem deleting n"

    
    
@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateForm()
    if form.validate_on_submit():
        current_user.event_name = form.event_name.data
        current_user.event_date = form.event_date.data
        current_user.event_timeStart = form.event_timeStart.data
        current_user.event_timeEnd = form.event_timeEnd.data
        e = Event(event_name = form.event_name.data, event_date = form.event_date.data, event_timeStart = form.event_timeStart.data, event_timeEnd = form.event_timeEnd.data, user = current_user)
        db.session.add(e)
        db.session.commit()
        flash('Your schedule has been saved')
        return redirect(url_for('create'))
    
    return render_template('create.html', title='Create', form=form)
    

    
@app.route('/edit/<e>', methods=['GET', 'POST'])
@login_required
def edit(e):
    Event_to_edit=  Event.query.get_or_404(e)
    
    form = CreateForm()
    if form.validate_on_submit():
        Event_to_edit.event_name = form.event_name.data
        Event_to_edit.event_date = form.event_date.data
        Event_to_edit.event_timeStart = form.event_timeStart.data
        Event_to_edit.event_timeEnd = form.event_timeEnd.data
        db.session.commit()
        flash('Your schedule has been updated')
        return redirect(url_for('create'))
    
    return render_template('edit.html', title='Edit', form=form,  Event_to_edit= Event_to_edit)

@app.route('/register', methods=['GET', 'POST'])
def register():
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/search/', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        event = form.eventName.data
        user = User.query.filter_by(username=current_user.username).first_or_404()
        even = Event.query.order_by('event_date', 'event_timeStart').filter(Event.user_id == user.id, Event.event_name.like(event)).all()
        return render_template('searchevent.html', title='Search Result', user = user, e=even, event=form.eventName)
    return render_template('search.html', title='Search', form=form)
    

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/calendar')
def calendar():
    # return render_template('calendar.html', title='Calendar')
    return redirect(url_for('userpage', username=current_user.username))
    
@app.route('/clock')
def clock():
    return render_template('clock.html', title='Clock')

@app.route('/about')
def about():
    return render_template('about.html', title='About')
    
 

  
