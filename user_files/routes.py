#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import request, Response, current_app
from user_files import app
from user_files.utils import is_authenticated
from werkzeug.utils import secure_filename, safe_join
import json
import base64
import io
import os
import shutil
from PIL import Image


@app.route("/", methods=['GET'])
def test_home():
    return "IT IS WORKING"


@app.route("/upload/<userid>", methods=['POST'])
@is_authenticated
def upload_file(userid):
    pdf_b64 = request.json['file']
    pdf_bytes = base64.b64decode(pdf_b64.encode('utf-8'))
    file_name = secure_filename(request.json['filename'])

    if not os.path.exists(os.path.join(current_app.root_path, "user_files_storage", userid)):
        os.makedirs(os.path.join(current_app.root_path, "user_files_storage", userid))

    file_path = os.path.join(current_app.root_path, "user_files_storage", userid, file_name)

    with open(file_path, "wb") as f:
        f.write(pdf_bytes)

    message = {"info": "file was saved"}
    resp = Response(json.dumps(message), status=200, mimetype='application/json')
    return resp


@app.route("/upload_profile/<userid>", methods=['POST'])
@is_authenticated
def upload_profile_pic(userid):
    im_b64 = request.json['image']
    img_bytes = base64.b64decode(im_b64.encode('utf-8'))
    file_name = secure_filename(request.json['filename'])

    if not os.path.exists(os.path.join(current_app.root_path, "user_files_storage", userid, "profile_pic")):
        os.makedirs(os.path.join(current_app.root_path, "user_files_storage", userid, "profile_pic"))

    file_path = os.path.join(current_app.root_path, "user_files_storage", userid, "profile_pic",
                             file_name)
    output_size = 125, 125
    i = Image.open(io.BytesIO(img_bytes))
    i.thumbnail(output_size)
    i.save(file_path)
    message = {"info": "file was saved"}
    resp = Response(json.dumps(message), status=200, mimetype='application/json')
    return resp


@app.route("/get/<userid>/<file_name>", methods=['GET'])
@is_authenticated
def get_file(userid, file_name):
    file_path = os.path.join(current_app.root_path, "user_files_storage", userid)
    if os.path.exists(safe_join(file_path, file_name)):
        with open(safe_join(file_path, file_name), "rb") as f:
            im_bytes = f.read()
        f_b64 = base64.b64encode(im_bytes).decode("utf8")
        message = {"file": f_b64, "filename": file_name}
        resp = Response(json.dumps(message), status=200, mimetype='application/json')
        return resp
    else:
        message = {"info": "couldn't find the file"}
        resp = Response(json.dumps(message), status=500, mimetype='application/json')
        return resp


@app.route("/get_profile/<userid>/<file_name>", methods=['GET'])
@is_authenticated
def get_profile(userid, file_name):
    file_path = os.path.join(current_app.root_path, "user_files_storage", userid, "profile_pic", file_name)
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            im_bytes = f.read()
        im_b64 = base64.b64encode(im_bytes).decode("utf8")
        img_url = "data:image/png;base64,"+str(im_b64)
        message = {"img_url": img_url}
        resp = Response(json.dumps(message), status=200, mimetype='application/json')
        return resp
    else:
        message = {"info": "couldn't find the file"}
        resp = Response(json.dumps(message), status=500, mimetype='application/json')
        return resp


@app.route("/delete_file/<userid>/<file_name>", methods=['POST'])
@is_authenticated
def delete_file(userid, file_name):
    file_path = os.path.join(os.path.join(current_app.root_path, "user_files_storage", userid, file_name))

    if os.path.exists(file_path):
        os.remove(file_path)
        message = json.dumps({"info": "File was deleted"})
        resp = Response(message, status=200, mimetype='application/json')
        return resp
    else:
        message = json.dumps({"info": "No file to delete"})
        resp = Response(message, status=500, mimetype='application/json')
        return resp


@app.route("/delete_profile_pic/<userid>/<file_name>", methods=['POST'])
@is_authenticated
def delete_profile(userid, file_name):
    file_path = os.path.join(os.path.join(current_app.root_path, "user_files_storage", userid),
                             "profile_pic", file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        message = json.dumps({"info": "File was deleted"})
        resp = Response(message, status=200, mimetype='application/json')
        return resp
    else:
        message = json.dumps({"info": "No file to delete"})
        resp = Response(message, status=500, mimetype='application/json')
        return resp


@app.route("/exists/<userid>/<file_name>", methods=['GET'])
@is_authenticated
def does_file_exists(userid, file_name):
    file_path = os.path.join(current_app.root_path, "user_files_storage", userid, file_name)

    if os.path.exists(file_path):
        message = json.dumps({"exists": True})
    else:
        message = json.dumps({"exists": False})
    return Response(message, status=200)


@app.route("/delete_user/<userid>", methods=['POST'])
@is_authenticated
def delete_user(userid):
    dir_to_delete = os.path.join(os.path.join(current_app.root_path, "user_files_storage", userid))
    if os.path.exists(dir_to_delete):
        shutil.rmtree(dir_to_delete)
        message = json.dumps({"info": "User was deleted"})
        resp = Response(message, status=200, mimetype='application/json')
        return resp
    else:
        message = json.dumps({"info": "No user to delete"})
        resp = Response(message, status=500, mimetype='application/json')
        return resp
