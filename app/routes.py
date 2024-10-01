from app import app
from flask import render_template, request, redirect, url_for

@app.route('/')
def index():
    return "Welcome to the PDF Processor"