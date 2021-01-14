import flask
from flask import request, jsonify, redirect, url_for, send_file
from flask_cors import CORS
from flask import session
from flask_sqlalchemy import SQLAlchemy
import db_helper
from werkzeug.utils import secure_filename
import os
from aws import upload_aws_lambda, download_aws_lambda, upload_dl_transfer
import uuid
import base64
import time

# from db_helper import User

# import database_helper as db_helperhelper
app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
CORS(app)

app.secret_key = "secertkey"


@app.route('/api/user/login', methods=['GET', 'POST'])
def login():
    response = {
        'status': '400',
        'success': False,
        'message': '',
        'token': ''
    }
    try:
        if request.method == 'POST':
            req = request.json
            print(req)
            if ('email' in req and 'password' in req) and \
                    (type(req['email'] == str) and
                        type(req['password'] == str)):
                if db_helper.login(req):
                    token = db_helper.generate_token(req['email'])
                    print(token)
                    response['status'] = '200'
                    response['success'] = True
                    response['message'] = 'login successfully'
                    response['token'] = token
                else:
                    response['message'] = 'email or password incorrect'
            else:
                response['message'] = 'incorrect payload format or content'
        else:
            response['message'] = 'incorrect http method'
        return jsonify(response)
    except Exception as e:
        print(e)
        return {'status': '500'}


@app.route('/api/user/register', methods=['GET', 'POST'])
def register():
    response = {
        'status': '400',
        'success': False,
        'message': ''
    }
    try:
        if request.method == 'POST':
            req = request.json
            if db_helper.create_user(req):
                response['status'] = '200'
                response['success'] = True
                response['message'] = 'user successfully registered'
            else:
                response['message'] = 'email taken'
        return jsonify(response)
    except Exception as e:
        print(e)
        return {'status': 500}


@app.route('/api/image/GanUpload', methods=["POST"])
def upload_gan_image():
    response = {
        'status': '400',
        'success': False,
        'message': ''
    }
    try:
        if request.method == 'POST':
            file = request.files['file']
            # print(file)
            style = request.form.get("style")
            filename = secure_filename(file.filename)
            # style = file.style
            # print(request.data)
            # print(style)
            ext = filename.split(".")[-1]
            hash_file = str(uuid.uuid4())
            destination = os.path.join("image", hash_file+"."+ext)
            file.save(destination)
            image_path = upload_dl_transfer(destination, style=style)
            # image_path = "./transfered/wave__859dda68-995f-42c6-97e4-ab8434fba796.jpg"

            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(
                    image_file.read()).decode("utf-8")
            print(encoded_string)
            return jsonify({"image": encoded_string})
            # download_aws_lambda("transfered/"+filename)
        return jsonify(response)
    except Exception as e:
        print(e)
        return {'status': 500}


@app.route('/api/image/upload', methods=["POST"])
def upload_image():
    response = {
        'status': '400',
        'success': False,
        'message': ''
    }
    bucket_dict = {"for-contract": "for-contract-texture-texture", "for-inv": "for-inv-texture-texture",
                   "for-mosaic": "for-mosaic-resized-texture", "for-sharp": "for-sharp-texture-texture", "for-text": "for-text-texture"}
    try:
        if request.method == 'POST':
            file = request.files['file']
            # print(file)
            style = request.form.get("style")
            new_bucket = bucket_dict[style]
            filename = secure_filename(file.filename)
            print(style)
            ext = filename.split(".")[-1]
            hash_file = str(uuid.uuid4())
            destination = os.path.join("image", hash_file+"."+ext)
            file.save(destination)
            upload_aws_lambda(path=destination, bucket=style)
            time.sleep(10)
            image_path = os.path.join("download", hash_file) + ".png"
            download_aws_lambda(
                path=image_path, new_key=hash_file+".png", new_bucket=new_bucket)
            # image_path = upload_dl_transfer(destination, style=style)
            # image_path = "./transfered/wave__859dda68-995f-42c6-97e4-ab8434fba796.jpg"

            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(
                    image_file.read()).decode("utf-8")
            print(encoded_string)
            return jsonify({"image": encoded_string})
            # download_aws_lambda("transfered/"+filename)
        return jsonify(response)
    except Exception as e:
        print(e)
        return {'status': 500}


@app.route('/api/user/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('current_user', None)

    return redirect(url_for('login'))


# for dubugging show all users


@app.route('/debug')
def show_table():
    users = User.query.all()
    message = ""
    for user in users:
        message += user.email
        message += '\t'
    return message


@app.route('/debug2', methods=["GET"])
def show_table2():
    print(request.headers.get('Authorization').split()[1])
    message = request.headers.get('Authorization')
    return message


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
