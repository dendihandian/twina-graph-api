from flask import Blueprint, jsonify, current_app

testApi = Blueprint('test', __name__)


@testApi.route('/test')
def test():

    current_app.logger.debug('debugged')
    current_app.logger.info('informed')
    current_app.logger.error('occurred')

    return jsonify({
        'message': 'Test completed'
    })
