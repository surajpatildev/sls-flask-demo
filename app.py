from flask import Flask, jsonify, make_response, request
from boto3 import client

app = Flask(__name__)


@app.route("/")
def hello_from_root():
    event = request.environ.get('serverless.event', {})
    print("event", event)
    claims = event.get("authorizer", {}).get("claims", {})

    conn = client('s3')  # again assumes boto.cfg setup, assume AWS S3
    keys = []
    for key in conn.list_objects(Bucket='notesaver-backend').get("Contents", []):
        print('bucket', key['Key'])
        keys.append(key['Key'])
    print("claims", claims)
    return jsonify(message='Hello from root!', keys=keys)


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
