from flask import Flask, send_from_directory
import os 
from Python_Bullet_Game import main_function

app = Flask(__name__)

@app.route('/')
def index(): 
    return main_function()