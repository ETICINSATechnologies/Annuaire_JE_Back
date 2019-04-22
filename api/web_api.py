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
            response = old_function(*args, **kwargs)
            if response is None:
                return '', 204
            if isinstance(response, (dict, list)):
                return jsonify(response)
            return response

        except LoginException:
            return jsonify({
                'message': 'authentication failed'
            }), 401

        except AuthError:
            return jsonify({
                'message': 'access denied'
            }), 403

        except (NotFound, sqlalchemy.orm.exc.NoResultFound):
            return jsonify({
                'message': 'no result found'
            }), 404

        except sqlalchemy.exc.IntegrityError:
            return jsonify({
                'message': 'integrity error'
            }), 422

        except FormatError:
            return jsonify({
                'message': 'incorrect file'
            }), 423

        except Exception as e:
            info_logger.error(e)

        return jsonify({
            'message': 'unexpected error'
        }), 500

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
        <h1 style="text-align:center"
          Welcome on Annuaire Back
        </h1>
        <div style="text-align:center"
          <p> This application was developed by ETIC INSA Technologies</p>
          <a href="https://github.com/ETICINSATechnologies/AnnuaireAncien_v2.0"
             style="text-align:center">Find us on Github!</a>
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
        MemberController.get_member_by_id(member_id),
        is_connected, request.headers.get('Authorization')
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


@app.route('/member/<int:member_id>/image', methods=['GET'])
def get_image(member_id):
    def get_member_image():
        image_location = find_image(member_id)
        if image_location:
            return send_from_directory(
                safe_join(os.getcwd(),
                          app.config['UPLOAD_FOLDER']),
                image_location)
        raise NotFound

    return send_response(
        lambda: get_member_image(),
        is_connected, request.headers.get('Authorization')
    )()


@app.route('/member/<int:member_id>/image', methods=['POST'])
def update_profile_picture(member_id):
    if request.files.get('file'):
        file = request.files['file']
        return send_response(
            lambda: save(file, member_id),
            is_own_resource, request.headers.get('Authorization'),
        )()


@app.route('/member/<int:member_id>/image', methods=['DELETE'])
def delete_profile_picture(member_id):
    return send_response(
        lambda: delete_image(member_id),
        is_own_resource, request.headers.get('Authorization'),
    )()


@app.route('/position', methods=['GET'])
def get_position():
    return send_response(
        lambda: MemberController.get_positions(),
        is_connected, request.headers.get('Authorization')
    )()


@app.route('/yearbook/upload', methods=['POST'])
def upload_file():
    if request.files.get('file'):
        file = request.files['file']
        return send_response(
            lambda: Controller.import_data(file),
            is_admin, request.headers.get('Authorization')
        )()


@app.route('/yearbook/download', methods=['GET'])
def download():
    Controller.export_data()
    return send_from_directory(
        safe_join(os.getcwd(), app.config['UPLOAD_FOLDER']),
        'annuaire.xlsx',
    )


if __name__ == '__main__':
    Controller.create_tables()
    app.run(debug=True, host='0.0.0.0')
