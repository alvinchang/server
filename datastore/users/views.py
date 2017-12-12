from flask import Blueprint, request, jsonify, json

from datastore.users.users_db import insert_user_in_db, DatabaseError
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

@users_blueprint.route("/create", methods=["POST"])
def add_user():
    payload = json.loads(request.data)
    users = payload.get(UserJsonKeys.USERS.value, [])
    user_objs = [User.from_json(user_json) for user_json in users]

    try:
        insert_user_in_db(user_objs)
    except DatabaseError as e:
        return jsonify({"error_msg": e.message}), 500

    return jsonify({"msg": 'created successfully'}), 201














