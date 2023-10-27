#!/usr/bin/env python3

from flask import request, session,jsonify,make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe

class Signup(Resource):
    def post(self):
        username = request.get_json()['username']
        password = request.get_json()['password']
        image_url = request.get_json()['image_url']
        bio = request.get_json()['bio']

        if username:
            new_user = User(username=username,image_url=image_url,bio=bio)
            new_user.password_hash = password

            db.session.add(new_user)
            db.session.commit()

            session['user_id']=new_user.id
            response=make_response(jsonify({
                "id":new_user.id,
                "username":new_user.username,
                "image_url":new_user.image_url,
                "bio":new_user.bio
            }),201)
            return response
        return {},422
class CheckSession(Resource):
    def get(self):
        if session.get('user_id'):
            user = User.query.filter(User.id == session['user_id']).first()
            response=make_response(jsonify({
                "id":user.id,
                "username":user.username,
                "image_url":user.image_url,
                "bio":user.bio
            }),201)
            return response
        else:
            return {}, 204

class Login(Resource):
    def post(self):
        username = request.get_json()['username']
        password = request.get_json()['password']
        user = User.query.filter(User.username == username).first()
        if user and user.authenticate(password):
            session['user_id'] = user.id
            response=make_response(jsonify({
                "id":user.id,
                "username":user.username,
                "image_url":user.image_url,
                "bio":user.bio
            }),200)
            return response
        else:
            return {},401
class Logout(Resource):
    def delete(self):
        if session.get("user_id"):
            session['user_id']=None
            return {},204
        else:
            return {},401

class RecipeIndex(Resource):
    pass

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)