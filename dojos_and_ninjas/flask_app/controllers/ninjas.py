from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.ninja import Ninja
from flask_app.models.dojo import Dojo

@app.route("/ninjas")
def ninja_display():
    dojos = Dojo.get_all()
    return render_template("ninja_add.html", dojos=dojos)

@app.route("/create_ninja", methods=['POST'])
def create_ninja():
    ninja = Ninja.save(request.form)
    return redirect(f"/dojos/{request.form['dojo_id']}")