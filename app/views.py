from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
@app.route('/targeting')
def index():
    return render_template('targetform.html')

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
