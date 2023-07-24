from flask import Flask, request
from neo4j_controller import db_functions

app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    return 'Welcome graph based splitwise'

@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'GET':
        user_id = request.args.get('user_id')
        return db_functions.get_user(user_id)

@app.route('/group', methods=['GET', 'POST'])
def group():
    if request.method == 'GET':
        group_id = request.args.get('group_id')
        return db_functions.get_group(group_id)


if __name__ == '__main__':
    app.run(debug=True)
