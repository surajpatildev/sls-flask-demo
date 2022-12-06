import logging
import os

from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

LOGGER = logging.getLogger(__name__)


@app.before_request
def set_logged_in_service_context():  # pylint:disable=inconsistent-return-statements
    is_offline = os.environ["IS_OFFLINE"]
    if is_offline:
        # If offline, set local user context
        request.service = "local"
        request.scopes = ["*"]
    else:
        # if via API gateway, use cognito to define scopes and service definitions
        context = request.environ.get("serverless.context")
        event = request.environ.get("serverless.event", {})

        claims = event.get("authorizer", {}).get("claims", {})
        client_id = claims.get("client_id")
        scope = claims.get("scope")
        if not all([client_id, scope]):
            return make_response(jsonify(error="Access Denied!"), 403)

        # setup context & event on request
        request.context = context
        request.event = event

        # strip scopes to pick schema names
        app_name = app.config["APP_NAME"]
        scopes = scope.replace(f"{app_name}/").split(" ")
        request.service = client_id
        request.scopes = scopes

    print(
        f"request context set: service - {request.service} & scopes - {request.scopes}"
    )


@app.route("/")
def home():
    print(f"v1.0: Service : {request.service}, Scopes: {request.scopes}")
    LOGGER.info("v1.0: Service : %s, Scopes: %s", request.service, request.scopes)
    return jsonify(message='Hello from root!')


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
