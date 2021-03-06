#!/usr/bin/env python3
# coding: utf8

import sqlalchemy.exc
import sqlalchemy.orm

from flask import Flask, send_from_directory, request, redirect
from flask.json import jsonify
from flask_cors import CORS

from controller.Controller import Controller
from controller.MemberController import MemberController
from util.log import info_logger
from util.send_email import Email, EmailError
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

        except LoginError:
            return jsonify({
                'message': 'unauthorized'
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

        except EmailError:
            return jsonify({
                'message': 'mail error'
            }), 502

        except Exception as e:
            print(e)
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

    raise LoginError


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


def get_member_image(member_id):
    image_location = find_image(member_id)
    if image_location:
        return send_from_directory(
            safe_join(os.getcwd(), app.config['UPLOAD_FOLDER']),
            image_location)
    raise NotFound


def get_my_id(authorization):
    return is_connected(authorization)['id']


@app.route('/api/')
def index():
    return redirect(
        'https://app.swaggerhub.com/apis/epsilon32/YearBook/v3.0.0#/'
    )


@app.route('/api/login', methods=['POST'])
def login_member():
    return send_response(
        lambda: MemberController.login(request.get_json())
    )()


@app.route('/api/member', methods=['POST'])
def create_member():
    return send_response(
        lambda: MemberController.create_member(request.get_json()),
        is_admin, request.headers.get('Authorization')
    )()


@app.route('/api/member', methods=['GET'])
def get_members():
    return send_response(
        lambda: MemberController.get_members(request.args),
        is_connected, request.headers.get('Authorization')
    )()


@app.route('/api/member/me', methods=['GET'])
def get_connected_member():
    return send_response(
        lambda:
        MemberController.get_member_by_id(
            get_my_id(request.headers.get('Authorization'))
        )
    )()


@app.route('/api/member/me', methods=['PUT'])
def update_connected_member():
    return send_response(
        lambda:
        MemberController.update_member(
            get_my_id(request.headers.get('Authorization')),
            request.get_json()),
    )()


@app.route('/api/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    return send_response(
        lambda:
        MemberController.get_member_by_id(member_id),
        is_connected, request.headers.get('Authorization')
    )()


@app.route('/api/member/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    return send_response(
        lambda:
        MemberController.update_member(member_id, request.get_json()),
        is_own_resource, request.headers.get('Authorization'), member_id
    )()


@app.route('/api/member/reset', methods=['POST'])
def update_temp_pass():
    return send_response(
        lambda:
        MemberController.update_temp_pass(request.get_json())
    )()


@app.route('/api/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    return send_response(
        lambda: MemberController.delete_member(member_id),
        is_admin, request.headers.get('Authorization')
    )()


@app.route('/api/member/me/image', methods=['GET'])
def get_connected_member_image():
    return send_response(
        lambda: get_member_image(
            get_my_id(request.headers.get('Authorization'))
        )
    )()


@app.route('/api/member/me/image', methods=['POST'])
def update_connect_member_image():
    if request.files.get('file'):
        file = request.files['file']
        return send_response(
            lambda: save(file, get_my_id(
                request.headers.get('Authorization')
            ))
        )()


@app.route('/api/member/me/image', methods=['DELETE'])
def delete_connected_member_image():
    return send_response(
        lambda: delete_image(get_my_id(
            request.headers.get('Authorization')
        ))
    )()


@app.route('/api/member/<int:member_id>/image', methods=['GET'])
def get_image(member_id):
    return send_response(
        lambda: get_member_image(member_id),
        is_connected, request.headers.get('Authorization')
    )()


@app.route('/api/member/<int:member_id>/image', methods=['POST'])
def update_member_image(member_id):
    if request.files.get('file'):
        file = request.files['file']
        return send_response(
            lambda: save(file, member_id),
            is_own_resource, request.headers.get('Authorization'),
        )()


@app.route('/api/member/<int:member_id>/image', methods=['DELETE'])
def delete_member_image(member_id):
    return send_response(
        lambda: delete_image(member_id),
        is_own_resource, request.headers.get('Authorization'),
    )()


@app.route('/api/position', methods=['GET'])
def get_position():
    return send_response(
        lambda: MemberController.get_positions(),
        is_connected, request.headers.get('Authorization')
    )()


@app.route('/api/yearbook/upload', methods=['POST'])
def upload_file():
    if request.files.get('file'):
        file = request.files['file']
        return send_response(
            lambda: Controller.import_data(file),
            is_admin, request.headers.get('Authorization')
        )()
    return jsonify({'message': 'missing file'}), 422


@app.route('/api/yearbook/download', methods=['GET'])
def download():
    Controller.export_data()
    return send_response(
        lambda: send_from_directory(
            safe_join(os.getcwd(), app.config['UPLOAD_FOLDER']),
            'annuaire.xlsx'),
        is_admin, request.headers.get('Authorization')
    )()


@app.route('/api/email/status', methods=['GET'])
def check_email_status():
    return send_response(
        lambda: Email.set_status(),
        is_admin, request.headers.get('Authorization')
    )()


@app.route('/api/email/validation', methods=['POST'])
def send_email_validation():
    if 'code' in request.form:
        return send_response(
            lambda: Email.create_token(request.form.get('code')),
            is_admin, request.headers.get('Authorization')
        )()
    return jsonify({'message': 'code error'}), 422


if __name__ == '__main__':
    Controller.create_tables()
    app.run(debug=True, host='0.0.0.0')
