#!/usr/bin/env python3
# coding: utf8

import sqlalchemy.exc
import sqlalchemy.orm

from flask import Flask, send_from_directory, request, safe_join
from flask.json import jsonify
from flask_cors import CORS

from controller.MemberController import MemberController
from util.Exception import LoginException
from util.upload import *

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)


def send_response(old_function):
    def new_function(*args, **kwargs):
        try:
            return jsonify(old_function(*args, **kwargs))
        except sqlalchemy.exc.IntegrityError:
            return 'integrity error', 422
        except sqlalchemy.orm.exc.NoResultFound:
            return 'no result found', 204
        except LoginException:
            return 'authentication failed', 401
        except Exception as e:
            print(e)
            info_logger.error(e)
            return "unexpected error", 500

    return new_function


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
        lambda: MemberController.create_member(request.get_json())
    )()


@app.route('/member', methods=['GET'])
def get_members():
    return send_response(
        lambda: MemberController.get_members(request.args)
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
        MemberController.update_member(member_id, request.get_json())
    )()


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    return send_response(
        lambda:
        MemberController.delete_member(member_id)
    )()


@app.route('/uploadFile/<int:doc_id>', methods=['GET', 'POST'])
def upload_file(doc_id):
    if request.method == 'POST':
        if request.files.get('file'):
            file = request.files['file']
            save_file(doc_id, file)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/getFile/<filename>')
def get_uploaded_file(filename):
    return send_from_directory(
        safe_join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)


if __name__ == '__main__':
    app.run(debug=True)
