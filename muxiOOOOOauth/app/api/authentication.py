# coding: utf-8

from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from . import api
from ..models import User, AnonymousUser


auth = HTTPBasicAuth()
# 现在用户的确在数据库里面


def unauthorized(message):
    response = jsonify({'error': 'unathorized', 'message': message})
    response.status_code = 401
    return response


@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token == '':
        g.current_user = AnonymousUser()
        return True

    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None

    user = User.query.filter_by(username=email_or_token).first()
    if not user:
        return False

    g.current_user = user
    g.token_used = False

    return user.verify_password(password)


@api.before_request
def before_request():
    pass


@api.route('/login/', methods=['POST', 'GET'])
@auth.login_required
def get_token():
    return jsonify({
        'uid': g.current_user.id
    })

