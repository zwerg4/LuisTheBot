from flask import Flask
from threading import Thread
 
app = Flask(__name__)
 
@app.route('/')
def index():
    return 'LuisTheBot Discord App is Running'
def run():
    app.run(host='0.0.0.0',port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

#Thread(target=app.run,args=("0.0.0.0",8080)).start()