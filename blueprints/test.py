from flask import Blueprint, jsonify, current_app

testApi = Blueprint('test', __name__)


@testApi.route('/', methods=['GET', 'POST'])
def base():
    return jsonify({
        'message': 'Don\'t worry, the app is working. But nothing in here.'
    })


@testApi.route('/test')
def test():

    current_app.logger.debug('debugged')
    current_app.logger.info('informed')
    current_app.logger.error('occurred')

    return jsonify({
        'message': 'Test completed'
    })
