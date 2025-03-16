from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import exc

from datetime import date

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///subscriptions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this for production

jwt = JWTManager(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True,)
    password = db.Column(db.String(100), nullable=False)

class SubscriptionPlan(db.Model):
    __tablename__ = 'subscription_plans'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)

class UserSubscription(db.Model):
    __tablename__ = 'user_subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False, index=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('subscription_plans.id'), nullable=False, index=True)
    start_date = db.Column(db.Date, nullable=False, index=True)
    end_date = db.Column(db.Date, nullable=True)
    active = db.Column(db.Boolean, default=True)

    user = db.relationship('User', back_populates='subscriptions')
    plan = db.relationship('SubscriptionPlan', back_populates='subscriptions')

User.subscriptions = db.relationship('UserSubscription', back_populates='user')
SubscriptionPlan.subscriptions = db.relationship('UserSubscription', back_populates='plan')

with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])

def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"msg": "Username and password required"}), 400

    hashed_password = generate_password_hash(password)
    
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "User already exists"}), 400
    
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"msg": "User registered successfully"}), 201



@app.route('/login', methods=['POST'])

def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password required"}), 400

    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    
    return jsonify({"access_token": access_token}), 200

@app.route('/plans', methods=['GET'])

def get_plans():
    plans = SubscriptionPlan.query.all()
    plan_list = [{"id": plan.id, "name": plan.name, "price": plan.price} for plan in plans]
    
    return jsonify(plan_list), 200



@app.route('/subscribe', methods=['POST'])

@jwt_required()

def subscribe_user():
    data = request.get_json()
    print("Received request data:", data)
    print("Request headers:", request.headers)

    if not data or 'plan_id' not in data:
        return jsonify({"msg": "Plan ID is required"}), 400

    current_user = get_jwt_identity()
    print("Current User ID from JWT:", current_user)

    plan = SubscriptionPlan.query.get(data['plan_id'])
    
    if not plan:
        return jsonify({"msg": "Plan not found"}), 404

    subscription = UserSubscription(user_id=current_user, plan_id=plan.id, start_date=date.today())
    db.session.add(subscription)
    db.session.commit()

    return jsonify({"msg": "Subscription created successfully"}), 201

if __name__ == '__main__':
    app.run()
