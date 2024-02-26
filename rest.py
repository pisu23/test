from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from snmp import snmp_request
import subprocess

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/user', methods=['POST'])
def add_user():
    username = request.json['username']
    email = request.json['email']
    new_user = User(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

@app.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/snmp')
def handle_request():
    return snmp_request()
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    # Start the SNMP simulator
    #subprocess.Popen(['snmpsimd.py', '--agent-udpv4-endpoint=127.0.0.1:5010'])
    # Terminal snmpsimd.py --agent-udpv4-endpoint=127.0.0.1:1024
    # Run the Flask server
    app.run(debug=True, port=5001)