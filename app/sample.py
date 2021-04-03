from flask import Flask, request, jsonify
from pymongo import MongoClient
import os, json, redis

# App
application = Flask(__name__)

# connect to MongoDB
mongoClient = MongoClient('mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_AUTHDB'])
db = mongoClient[os.environ['MONGODB_DATABASE']]

# connect to Redis
redisClient = redis.Redis(host=os.environ.get("REDIS_HOST", "localhost"), port=os.environ.get("REDIS_PORT", 6379), db=os.environ.get("REDIS_DB", 0))

@application.route('/')
def index():
    body = '<h2>Alphabet Guessing Game V.1.0</h2>'
    col_game = db.game
    game = col_game.find_one()
    if game != None:
        question_text = ' '.join(game['question'])
        body += "Please Choose A or B or C or D to add to the question."
        body += '<br>'
        body += 'Question: ' + question_text
        body += '<br> <br>'
        body += 'Choose:  <a href="/A"><button> A </button></a>' 
        body += '<a href="/B"><button> B </button></a>'
        body += '<a href="/C"><button> C </button></a>'
        body += '<a href="/D"><button> D </button></a>'
        if game['index'] == 4:
            col_game.update_one({'stage': 1}, {"$set": {"mode"  : 1}})
            col_game.update_one({'stage': 1}, {"$set": {"index" : 0}})
            body += '<br> <br>'
            body += '<a href="/gameplay"><button> Finish </button></a>'
            body += '<a href="/reset"><button> Reset </button></a>'
    else:
        mydict = {
            "stage": 1, 
            "question": ["_","_","_","_"], 
            "char_remain": ["*","*","*","*"], 
            "answer": [], 
            "fail": 0,
            "index": 0, 
            "mode": 0
            }
        col_game.insert_one(mydict)
        body += "Please refresh to play the game."
    return body

@application.route('/A')
def chooseA():
    col_game = db.game
    game = col_game.find_one()
    if game['mode'] == 0:
        current_index = game["index"]
        col_game.update_one({'stage': 1}, {"$set": {"question." + str(current_index) : 'A'}})
        current_index += 1
        col_game.update_one({'stage': 1}, {"$set": {"index" : current_index}})
        return index()
    if game['mode'] == 1:
        current_index = game["index"]
        current_fail = game["fail"]
        if game['question'][current_index] == 'A':
            col_game.update_one({'stage': 1}, {"$set": {"answer." + str(current_index) : 'A'}})
            current_index += 1
            col_game.update_one({'stage': 1}, {"$set": {"index" : current_index}})
            col_game.update_one({'stage': 1}, { "$set": { 'char_remain.' + str(current_index): "" }})
        else:
            current_fail += 1
            col_game.update_one({'stage': 1}, {"$set": {"fail": current_fail}})
        return gameplay()

@application.route('/B')
def chooseB():
    col_game = db.game
    game = col_game.find_one()
    if game['mode'] == 0:
        current_index = game["index"]
        col_game.update_one({'stage': 1}, {"$set": {"question." + str(current_index) : 'B'}})
        current_index += 1
        col_game.update_one({'stage': 1}, {"$set": {"index" : current_index}})
        return index()
    if game['mode'] == 1:
        current_index = game["index"]
        current_fail = game["fail"]
        if game['question'][current_index] == 'B':
            col_game.update_one({'stage': 1}, {"$set": {"answer." + str(current_index) : 'B'}})
            current_index += 1
            col_game.update_one({'stage': 1}, {"$set": {"index" : current_index}})
            col_game.update_one({'stage': 1}, { "$set": { 'char_remain.' + str(current_index): "" }})
        else:
            current_fail += 1
            col_game.update_one({'stage': 1}, {"$set": {"fail": current_fail}})
        return gameplay()
    
@application.route('/C')
def chooseC():
    col_game = db.game
    game = col_game.find_one()
    if game['mode'] == 0:
        current_index = game["index"]
        col_game.update_one({'stage': 1}, {"$set": {"question." + str(current_index) : 'C'}})
        current_index += 1
        col_game.update_one({'stage': 1}, {"$set": {"index" : current_index}})
        return index()
    if game['mode'] == 1:
        current_index = game["index"]
        current_fail = game["fail"]
        if game['question'][current_index] == 'C':
            col_game.update_one({'stage': 1}, {"$set": {"answer." + str(current_index) : 'C'}})
            current_index += 1
            col_game.update_one({'stage': 1}, {"$set": {"index" : current_index}})
            col_game.update_one({'stage': 1}, { "$set": { 'char_remain.' + str(current_index): "" }})
        else:
            current_fail += 1
            col_game.update_one({'stage': 1}, {"$set": {"fail": current_fail}})
        return gameplay()

@application.route('/D')
def chooseD():
    col_game = db.game
    game = col_game.find_one()
    if game['mode'] == 0:
        current_index = game["index"]
        col_game.update_one({'stage': 1}, {"$set": {"question." + str(current_index) : 'D'}})
        current_index += 1
        col_game.update_one({'stage': 1}, {"$set": {"index" : current_index}})
        return index()
    if game['mode'] == 1:
        current_index = game["index"]
        current_fail = game["fail"]
        if game['question'][current_index] == 'D':
            col_game.update_one({'stage': 1}, {"$set": {"answer." + str(current_index) : 'D'}})
            current_index += 1
            col_game.update_one({'stage': 1}, {"$set": {"index" : current_index}})
            col_game.update_one({'stage': 1}, { "$set": { 'char_remain.' + str(current_index): "" }})
        else:
            current_fail += 1
            col_game.update_one({'stage': 1}, {"$set": {"fail": current_fail}})
        return gameplay()

@application.route('/gameplay')
def gameplay():
    col_game = db.game
    game = col_game.find_one()
    if game['question'] == game['answer']:
        return gameover()
    ans_text = ' '.join(game['answer'])
    char_remain_text = ' '.join(game['char_remain'])
    body = '<h2>Alphabet Guessing Game V.1.0</h2>'
    body += "Please Choose A or B or C or D to guess."
    body += '<br> <br> '
    body += 'Answer: ' + ans_text
    body += '<br>'
    body += 'Character(s) remaining: ' + char_remain_text
    body += '<br> <br>'
    body += 'Choose:  <a href="/A"><button> A </button></a>' 
    body += '<a href="/B"><button> B </button></a>'
    body += '<a href="/C"><button> C </button></a>'
    body += '<a href="/D"><button> D </button></a>'
    body += '<br> <br>'
    body += 'Fails: ' + str(game["fail"])
    return body

@application.route('/reset')
def reset():
    col_game = db.game
    col_game.update_one({'stage': 1}, {"$set": {"question": ["_","_","_","_"], "mode": 0}})
    return index()

@application.route('/gameover')
def gameover():
    col_game = db.game
    game = col_game.find_one()
    body = '<h2>Alphabet Guessing Game V.1.0</h2>'
    body += '<b>You win!</b>'
    body += '<br> <br> '
    body += '<b>Fails: </b>' + str(game['fail'])
    body += '<br> <br> '
    body += '<a href="/again"><button> Play again! </button></a>'
    return body

@application.route('/again')
def again():
    col_game = db.game
    mydict = {
        "stage": 1, 
        "question": ["_","_","_","_"], 
        "char_remain": ["*","*","*","*"], 
        "answer": [], 
        "fail": 0,
        "index": 0, 
        "mode": 0
    }
    col_game.update_one({'stage': 1}, {"$set": mydict})
    return index()


@application.route('/sample')
def sample():
    doc = db.test.find_one()
    # return jsonify(doc)
    body = '<div style="text-align:center;">'
    body += '<h1>Python</h1>'
    body += '<p>'
    body += '<a target="_blank" href="https://flask.palletsprojects.com/en/1.1.x/quickstart/">Flask v1.1.x Quickstart</a>'
    body += ' | '
    body += '<a target="_blank" href="https://pymongo.readthedocs.io/en/stable/tutorial.html">PyMongo v3.11.2 Tutorial</a>'
    body += ' | '
    body += '<a target="_blank" href="https://github.com/andymccurdy/redis-py">redis-py v3.5.3 Git</a>'
    body += '</p>'
    body += '</div>'
    body += '<h1>MongoDB</h1>'
    body += '<pre>'
    body += json.dumps(doc, indent=4)
    body += '</pre>'
    res = redisClient.set('Hello', 'World')
    if res == True:
      # Display MongoDB & Redis message.
      body += '<h1>Redis</h1>'
      body += 'Get Hello => '+redisClient.get('Hello').decode("utf-8")
    return body

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("FLASK_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("FLASK_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)