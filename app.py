from flask import Flask, jsonify, request, make_response, redirect, render_template
import jwt
import datetime
from functools import wraps
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecretkey'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') #http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated

@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'secret':
        token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=15)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

@app.route('/users',methods=['GET'])
@token_required
def users():
    if request.method == 'GET':
        storage_path = 'users.json'
        with open(storage_path, 'r') as f:
            try:
                users_data = json.load(f)
                print('loaded that: ', users_data)
            except Exception as e:
                print("got %s on json.load()" % e)
        userdetails = []
        for user in users_data:
            userdetails.append([user['user_id'], user['name'], user['email']])
        return render_template('show.html', userdetails=userdetails)

@app.route('/albums',methods=['GET'])
@token_required
def albums():
    if request.method == 'GET':
        storage_path = 'users.json'
        with open(storage_path, 'r') as f:
            try:
                users_data = json.load(f)
                print('loaded that: ', users_data)
            except Exception as e:
                print("got %s on json.load()" % e)
        all_albums = []
        for user in users_data:
            for album in user['albums']:
                all_albums.append([album['album_id'],album['title']])
        return render_template('albums.html', albumdetails=all_albums)

@app.route('/albums/<int:album_id>',methods=['GET'])
@token_required
def get_album(album_id):
    if request.method == 'GET':
        storage_path = 'users.json'
        with open(storage_path, 'r') as f:
            try:
                users_data = json.load(f)
                print('loaded that: ', users_data)
            except Exception as e:
                print("got %s on json.load()" % e)
        all_albums = []
        for user in users_data:
            for album in user['albums']:
                if album['album_id'] == album_id:
                    all_albums.append([album['album_id'], album['title']])
        return render_template('albums.html', albumdetails=all_albums)

@app.route('/photos',methods=['GET'])
@token_required
def photos():
    if request.method == 'GET':
        storage_path = 'users.json'
        with open(storage_path, 'r') as f:
            try:
                users_data = json.load(f)
                print('loaded that: ', users_data)
            except Exception as e:
                print("got %s on json.load()" % e)
        all_photos = []
        for user in users_data:
            for album in user['albums']:
                album_id = album['album_id']
                for photo in album["photos"]:
                    all_photos.append([photo['photo_id'], album_id])
        return render_template('photos.html', photodetails=all_photos)

@app.route('/photos/<int:photo_id>',methods=['GET'])
@token_required
def get_photo(photo_id):
    if request.method == 'GET':
        storage_path = 'users.json'
        with open(storage_path, 'r') as f:
            try:
                users_data = json.load(f)
                print('loaded that: ', users_data)
            except Exception as e:
                print("got %s on json.load()" % e)
        all_photos = []
        for user in users_data:
            for album in user['albums']:
                album_id = album['album_id']
                for photo in album["photos"]:
                    if photo['photo_id'] == photo_id:
                        all_photos.append([photo['photo_id'], album_id])
        return render_template('photos.html', photodetails=all_photos)

if __name__ == '__main__':
    app.run(debug=True)


