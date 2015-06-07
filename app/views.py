from flask import render_template, flash, redirect
from app import app
from .targetform import TargetForm
from .jfweb import process_web_form

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/targeting', methods=['GET', 'POST'])
def targeting():
    targetform = TargetForm()
    if targetform.validate_on_submit():
        return redirect('/result')
    return render_template('targetform.html', targetform=targetform)

@app.route('/about')
@app.route('/about-1')
def about():
    return render_template('about1.html')

@app.route('/about-2')
def about2():
    return render_template('about2.html')

@app.route('/about-3')
def about3():
    return render_template('about3.html')

@app.route('/result')
def result():
    return render_template('result.html')
