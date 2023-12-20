# Define simple app for user registration and sign in

from flask import Flask, jsonify, request
import json
import bcrypt  # hashing algorithm

app = Flask(__name__)

# Let us load data from JSON files
with open("users.json", "r") as users_file:
    users = json.load(users_file)

with open("authorized.json", "r") as authorized_file:
    # here are the users which are currently logged in
    authorized = json.load(authorized_file)


# define function to check email availability
def check_email(email):
    for user in users:
        if user['email'] == email:
            return user
    return None


# define function to remove user from authorized list after logging out
def check_auth_by_id_and_remove(user_id):
    for user in authorized:
        if user["id"] == user_id:
            authorized.remove(user)
            return 'The user is removed from authorized list.'
    return None


@app.route('/app/register', methods=['POST'])
def register():
    req = request.json
    if "username" in req and "email" in req and "password" in req:
        # case when email is already used
        if check_email(req['email']):
            return jsonify("The email is already used"), 409
        # case when email is not used
        else:
            username = req['username']
            email = req['email']
            password = req['password'].encode('utf-8')
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            new_user_id = len(users) + 1
            new_user_info = {"id": new_user_id, "username": username, "email": email,
                             "password": hashed_password.decode('utf-8')}
            users.append(new_user_info)
            with open("users.json", 'w') as users_file:
                json.dump(users, users_file)
            return jsonify("You are successfully registered!"), 201
    # case when the required data is not provided fully or partially
    else:
        return jsonify(
            "Data is invalid, please provide all the required data, including username, email, password"), 400


@app.route('/app/login', methods=['POST'])
def login():
    req = request.json
    if "email" in req and "password" in req:
        # case when user exist
        user_info = check_email(req['email'])
        if user_info:
            email = req['email']
            password = req['password'].encode('utf-8')
            # check if stored hashed password and provided password during login are correct or not
            if bcrypt.checkpw(password, user_info['password'].encode('utf-8')):
                login_user = {"id": user_info['id'], "email": user_info['email']}
                authorized.append(login_user)
                with open("authorized.json", 'w') as authorized_file:
                    json.dump(authorized, authorized_file)
                return jsonify({"Login is successful, provided password is correct. Here is the user information: ":
                                    [user_info['username'], user_info['email']]}), 200
            # case when the provided password is not correct
            else:
                return jsonify("Your provided password is not correct."), 401

        # case when there is no such user
        else:
            return jsonify("You are not registered, so you can not log in, first go and register."), 404
    # case when needed data is not provided
    else:
        return jsonify("Data is invalid, please provide all the required data, including email, password"), 400


@app.route('/app/logout', methods=['POST'])
def logout():
    req = request.json
    if "user_id" in req:
        auth = check_auth_by_id_and_remove(req['user_id'])
        if auth:
            # user in no more logged in authorized
            with open("authorized.json", "w") as authorized_file:
                json.dump(authorized, authorized_file)
            return jsonify({"The given user is no more authorized, you can see remaining authorized users": authorized})
        # case when provided user_id is not in the authorized list
        else:
            return jsonify("The provided user_id is not authorized or logged in, so you can not log out.")
    else:
        return jsonify("Please provide user_id to be able to log out"), 400


@app.route('/app', methods=['GET'])
def get_users():
    return jsonify({"Here is the list of all registered and logged in users of the app":
                        {"registered users": users, "logged in users": authorized}})


if __name__ == "__main__":
    app.run(debug=True)
