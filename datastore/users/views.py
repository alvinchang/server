from flask import Blueprint, request, jsonify, json

from datastore.users.users_db import insert_user_in_db, DatabaseError, get_user_in_db, modify_user_email_in_db, \
    delete_user_in_db
from responses.json_responses import JsonErrorResponse, JsonSuccessResponse, HttpStatusCode
from users.users import UserJsonKeys, User

users_blueprint = Blueprint("users", __name__)


"""
{
 'USERS': [
   {
    'user_name': 'JohnDoe',
    'first_name': 'John',
    'last_name': 'Doe',
    'email': 'JohnDoe@email.com'
   }, ...
}

"""


@users_blueprint.route("/create_user", methods=["POST"])
def add_user():
    payload = json.loads(request.data)
    users = payload.get(UserJsonKeys.USERS.value, [])
    user_objs = [User.from_json(user_json) for user_json in users]

    try:
        insert_user_in_db(user_objs)
    except DatabaseError as e:
        return JsonErrorResponse(HttpStatusCode.INTERNAL_SERVER_ERROR, e).to_response
    except Exception as e:
        return JsonErrorResponse(HttpStatusCode.INTERNAL_SERVER_ERROR, e).to_response

    return JsonSuccessResponse(HttpStatusCode.RESOURCE_CREATED, "users created successfully").to_response


@users_blueprint.route("/get_user/<string: username>", methods=["GET"])
def get_user():
    user_name = request.args.get('username', None)

    try:
        user = get_user_in_db(user_name)
        return jsonify({
            UserJsonKeys.USER_NAME.VALUE: user.user_name

        }), HttpStatusCode.OK.value
    except DatabaseError as e:
        return JsonErrorResponse(HttpStatusCode.INTERNAL_SERVER_ERROR, e).to_response
    except Exception as e:
        return JsonErrorResponse(HttpStatusCode.INTERNAL_SERVER_ERROR, e).to_response


@users_blueprint.route("/update_user/<string: username>/<string: new_email>", methods=["PUT"])
def update_user():
    user_name = request.args.get('username', None)
    new_email = request.args.get('new_email', None)
    try:
        modify_user_email_in_db(user_name, new_email)
        return JsonSuccessResponse(HttpStatusCode.RESOURCE_CREATED, "users updated successfully").to_response
    except DatabaseError as e:
        return JsonErrorResponse(HttpStatusCode.INTERNAL_SERVER_ERROR, e).to_response
    except Exception as e:
        return JsonErrorResponse(HttpStatusCode.INTERNAL_SERVER_ERROR, e).to_response


@users_blueprint.route("/delete/<string: username>", methods=["DEL"])
def delete_user():
    user_name = request.args.get('username', None)
    try:
        delete_user_in_db(user_name)
        return JsonSuccessResponse(HttpStatusCode.OK, "users deleted successfully").to_response
    except DatabaseError as e:
        return JsonErrorResponse(HttpStatusCode.INTERNAL_SERVER_ERROR, e).to_response
    except Exception as e:
        return JsonErrorResponse(HttpStatusCode.INTERNAL_SERVER_ERROR, e).to_response
















