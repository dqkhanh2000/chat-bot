from flask import Flask, render_template, request
import os
from bot_lib import *

template_dir = os.path.abspath('./public')
app = Flask(__name__,  template_folder=template_dir, static_folder=template_dir)
HOST = "0.0.0.0"
PORT = 5000
DEBUG = False



@app.route('/')
def hello_world():
  return render_template("index.html")

@app.route('/api/chat', methods=['POST'])
def chat():
  question = request.form['question']
  return str(get_response(question))

if __name__ == '__main__':
  load_data()
  print("LOAD DATA DONE")
  app.run(HOST, PORT, DEBUG)
