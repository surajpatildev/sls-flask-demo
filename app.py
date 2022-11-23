from flask import Flask, jsonify, make_response, request

app = Flask(__name__)


@app.route("/")
def hello_from_root():
    event = request.environ.get('serverless.event')
    print("event", event)
    claims = event.get("authorizer", {}).get("claims", {})
    print("claims", claims)
    return jsonify(message='Hello from root!', claims=claims)


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
