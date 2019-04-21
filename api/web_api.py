#!/usr/bin/env python3
# coding: utf8

import sqlalchemy.exc
import sqlalchemy.orm

from flask import Flask, send_from_directory, request
from flask.json import jsonify
from flask_cors import CORS

from controller.Controller import Controller
from controller.MemberController import MemberController
from util.upload import *
from util.Exception import *
from util.encryption import *

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)


def send_response(old_function, authorization_function=None,
                  authorization=None, resource_id=None):
    def new_function(*args, **kwargs):

        try:
            if authorization_function:
                authorization_function(authorization, resource_id)
            return jsonify(old_function(*args, **kwargs))

        except sqlalchemy.orm.exc.NoResultFound:
            return 'no result found', 204

        except LoginException:
            return 'authentication failed', 401

        except AuthError:
            return 'access denied', 403

        except sqlalchemy.exc.IntegrityError:
            return 'integrity error', 422

        except FormatError:
            return 'incorrect file', 423

        except Exception as e:
            print(e)
            info_logger.error(e)

        return "unexpected error", 500

    return new_function


def is_connected(*args):
    jwt = args[0]

    if jwt:
        payload = jwt_decode(jwt)
        if payload:
            return payload

    raise AuthError


def is_own_resource(*args):
    jwt = args[0]
    resource_id = args[1]
    payload = is_connected(jwt)

    if payload['username'] != 'admin' and payload['id'] != resource_id:
        raise AuthError

    return True


def is_admin(*args):
    jwt = args[0]

    payload = is_connected(jwt)
    if payload['username'] != 'admin':
        raise AuthError

    return True


@app.route('/')
def index():
    return ''' 
    <!doctype html>  
    <html>  
      <body>          
        <h1 style="text-align:center">  
          Welcome on Annuaire Back 
        </h1>  
        <div style="text-align:center">  
          <p> This application was developed by ETIC INSA Technologies</p>  
          <a href="https://github.com/ETICINSATechnologies/AnnuaireAncien_v2.0"   
             style="text-align:center"> Find us on Github! </a>  
        </div>  
      </body>  
    </html>  
    '''


@app.route('/login', methods=['POST'])
def login_member():
    return send_response(
        lambda: MemberController.login(request.get_json())
    )()


@app.route('/member', methods=['POST'])
def create_member():
    return send_response(
        lambda: MemberController.create_member(request.get_json()),
        is_admin, request.headers.get('Authorization')
    )()


@app.route('/member', methods=['GET'])
def get_members():
    return send_response(
        lambda: MemberController.get_members(request.args),
        is_connected, request.headers.get('Authorization')
    )()


@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    return send_response(
        lambda:
        MemberController.get_member_by_id(member_id)
    )()


@app.route('/member/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    return send_response(
        lambda:
        MemberController.update_member(member_id, request.get_json()),
        is_own_resource, request.headers.get('Authorization'), member_id
    )()


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    return send_response(
        lambda: MemberController.delete_member(member_id),
        is_admin, request.headers.get('Authorization')
    )()


@app.route('/member/<int:member_id>/image', methods=['GET', 'POST'])
def update_profile_picture(member_id):
    if is_own_resource(request.headers.get('Authorization'), member_id):
        if request.method == 'POST':
            try:
                if request.files.get('file'):
                    file = request.files['file']
                    save_file(file, member_id)
                    return 'Success'
            except Exception as e:
                info_logger.error(e)

            return "unexpected error", 500

        return '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form method=post enctype=multipart/form-data>
              <p><input type=file name=file>
                 <input type=submit value=Upload>
            </form>
            '''


@app.route('/member/<int:member_id>/get_image', methods=['GET'])
def get_image(member_id):
    if is_own_resource(request.headers.get('Authorization'), member_id):
        image_location = find_image(member_id)
        if image_location:
            return send_from_directory(
                safe_join(os.getcwd(), app.config['UPLOAD_FOLDER']),
                image_location
            )

        return 'not found', 204

    return 'access denied', 403


@app.route('/position', methods=['GET'])
def get_position():
    return send_response(
        lambda: MemberController.get_positions()
    )()


@app.route('/yearbook/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            if request.files.get('file'):
                file = request.files['file']
                save_file(file)
                Controller.import_data()
                return 'Success'
        except FormatError:
            return 'incorrect file', 423
        except Exception as e:
            info_logger.error(e)

        return "unexpected error", 500

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/yearbook/download', methods=['GET'])
def download():
    Controller.export_data()
    return send_from_directory(
        safe_join(os.getcwd(), app.config['UPLOAD_FOLDER']),
        'annuaire.xlsx'
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
