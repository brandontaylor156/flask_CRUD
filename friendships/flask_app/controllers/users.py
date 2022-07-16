from flask_app import app, render_template, request, redirect
from flask_app.models import user as user_mod
from pprint import pprint

@app.route("/")
def index():
    return redirect("/friendships")

@app.route("/friendships", methods=['GET', 'POST'])
def friendships():
    if request.method == 'POST':

        if request.form['which_form'] == 'insert_user':
            data = {
                "first_name":request.form['first_name'],
                "last_name":request.form['last_name']
            }
            user_mod.User.insert_user(data)

        elif request.form['which_form'] == 'insert_friendship':
            data = {
                "user_id": request.form['user_id'],
                "friend_id":request.form['friend_id']
            }
            user_mod.User.insert_friendship(data)

          
    users = user_mod.User.select_users()

    friendships = []
    for user in users:
        data = {
            'id': user.id
        }
        if user_mod.User.select_friendships(data):
            friendships.append(user_mod.User.select_friendships(data))

    return render_template("friendships.html", users = users, friendships=friendships)



