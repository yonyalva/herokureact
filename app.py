import os
from flask import Flask, render_template, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

from  models import setup_db, Actor, Movie
# from  auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response


    ## ROUTES

    @app.route('/')
    def hi():
        return render_template('casting-agency/index.html')
        # return "Hi!, this is only being used as a backeend API"

    @app.route('/actors')
    # creates the actors endpoint
    def get_actors():
            actors = Actor.query.all()
            formatted_actors = [actor.format() for actor in actors]

            if len(formatted_actors) == 0:
                abort(404)
            # display results
            return jsonify({
            'success':True,
            'actors': formatted_actors
                })

    @app.route('/movies')
    # creates the movies endpoint
    def get_movies():
            movies = Movie.query.all()
            formatted_movies = [movie.format() for movie in movies]

            if len(formatted_movies) == 0:
                abort(404)
            
            # display results
            return jsonify({
            'success':True,
            'movies': formatted_movies
                })

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    # @requires_auth('delete:movies')
    # creates the delete movies endpoint
    def delete_movie(movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            if movie is None:
                abort(404)

            movie.delete()

            # display results
            return jsonify({
            'success':True,
            'deleted': movie_id
                })
            
        except:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    # @requires_auth('delete:actors')
    # creates the delete actors endpoint
    def delete_actor(actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

            if actor is None:
                abort(404)

            actor.delete()

            # display results
            return jsonify({
            'success':True,
            'deleted': actor_id
                })
            
        except:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    # @requires_auth('patch:movies')
    def movies_patch(movie_id):
        body = request.get_json()
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404)
            if 'title' in body:
                movie.title = body.get('title')
            if 'release_date' in body:
                movie.release_date = body.get('release_date')

            movie.update()

            return jsonify({
                "success": True
            })
        except:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    # @requires_auth('patch:actors')
    def actors_patch(actor_id):
        body = request.get_json()
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if actor is None:
                abort(404)
            if 'name' in body:
                actor.name = body.get('name')
            if 'age' in body:
                actor.age = body.get('age')
            if 'gender' in body:
                actor.gender = body.get('gender')

            actor.update()

            return jsonify({
                "success": True
            })
        except:
            abort(422)

    @app.route('/movies_new', methods=['POST'])
    # @requires_auth('post:movies')
    # create a new movie endpoint
    def new_movie():
        body = request.get_json()

        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        try:
            movie = Movie(title=new_title, release_date=new_release_date)
            movie.insert()

            # display results
            return jsonify({
            'success':True,
            'movie': movie.id
                }) 
        except:
            abort(422)

    @app.route('/actors_new', methods=['POST'])
    # @requires_auth('post:actors')
    # create a new actor endpoint
    def new_actor():
        body = request.get_json()

        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        try:
            actor = Actor(name=new_name, age=new_age, gender=new_gender)
            actor.insert()

            # display results
            return jsonify({
            'success':True,
            'movie': actor.id
                }) 
        except:
            abort(422)

    # app error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Not found"
            }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
        "success": False, 
        "error": 400,
        "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
        "success": False, 
        "error": 500,
        "message": "Internal Server Error"
        }), 500

    @app.errorhandler(405)
    def not_allow(error):
        return jsonify({
        "success": False, 
        "error": 405,
        "message": "Method Not Allowed"
        }), 405

    return app

app = create_app()
