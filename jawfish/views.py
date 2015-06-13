# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, send_file
from jawfish import app
from .targetform import TargetForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/targeting', methods=['GET', 'POST'])
def targeting():
    targetform = TargetForm()
    return render_template('targetform.html', targetform=targetform)

@app.route('/about')
@app.route('/about-1')
def about():
    return render_template('about1.html', title='What is Jawfish?')

@app.route('/about-2')
def about2():
    return render_template('about2.html', title='Parts of the targeting form')

@app.route('/about-3')
def about3():
    return render_template('about3.html', title='Ending notes')

@app.route('/result')
def result():
    return render_template('result.html', title='Jawfish -')

@app.route('/jf-web.py')
def jfweb():
    return send_file('jf-web.py')
