from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_cors import CORS  

app = Flask(__name__)
CORS(app, resources={r"/video_feed": {"origins": "http://localhost:8080"}})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8080')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    return response



@app.route('/video_feed', methods=['POST'])
def video_feed():
    import agePredict
    client_name, client_age = agePredict.agePredict()
    response_data = {'message': '연령 예측이 성공적으로 완료되었습니다!'}
    return jsonify(response_data), 200

if __name__ == '__main__':
    app.run(host='localhost', port=5000)