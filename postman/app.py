from flask import Flask, render_template, url_for
import controller.user_controller as user_controller

app=Flask(__name__)

@app.route('/')
def index():
    return "This is the Home page"
