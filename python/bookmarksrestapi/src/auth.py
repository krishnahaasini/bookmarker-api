from flask import Blueprint, request,jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from src.database import User,db
from src.constants import http_status_codes
import validators
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flasgger import Swagger, swag_from


auth=Blueprint('auth',__name__,url_prefix='/api/v1/auth')

@auth.post('/register')
@swag_from('./docs/auth/register.yaml')
def register():
    username=request.json['username']
    email=request.json['email']
    password=request.json['password']

    if len(password)<6:
        return jsonify({'error': 'Password is too short'}), http_status_codes.HTTP_400_BAD_REQUEST

    if len(username)<3:
        return jsonify({'error':'Username too short'}), http_status_codes.HTTP_400_BAD_REQUEST

    if not username.isalnum() or ' ' in username:
        return jsonify({'error':'Username should be alphanumeric also no spaces'}), http_status_codes.HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error':'Email is not valid'}), http_status_codes.HTTP_400_BAD_REQUEST
    
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error':'Email is already taken'}), http_status_codes.HTTP_409_CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error':'Username is already taken'}), http_status_codes.HTTP_409_CONFLICT

    pwd_hash=generate_password_hash(password)

    user=User(username=username, password=pwd_hash, email=email) 

    db.session.add(user)
    db.session.commit()

    return jsonify(
        {'message': 'User Created',
         'user':{'username':username, 'email':email}
        }
    ),http_status_codes.HTTP_201_CREATED



@auth.post('/login')
@swag_from('./docs/auth/login.yaml')
def login():
    email=request.json.get('email','')
    password=request.json.get('password','')

    user=User.query.filter_by(email=email).first()
    if user:
        is_pass_correct=check_password_hash(user.password,password)
        
        if is_pass_correct:
            refresh=create_refresh_token(identity=user.id)
            access=create_access_token(identity=user.id)

            return jsonify({
                'user': {
                    'refresh': refresh,
                    'access': access,
                    'username': user.username,
                    'email': user.email
                } 
            }), http_status_codes.HTTP_200_OK
    return jsonify({'error':'Wrong credentials'}), http_status_codes.HTTP_401_UNAUTHORISED


@auth.get('/me')
@jwt_required()
def get_me():
    """get me function
    """
    user_id=get_jwt_identity()
    user=User.query.filter_by(id=user_id).first()
    return jsonify({
        'username':user.username,
        'email':user.email
    }), http_status_codes.HTTP_200_OK



@auth.get('/token/refresh')
@jwt_required()
def refresh_users_token():
    identity=get_jwt_identity()
    access=create_access_token(identity=identity)
    return jsonify({
        'access':access
    }),http_status_codes.HTTP_200_OK



