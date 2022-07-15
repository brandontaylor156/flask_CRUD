from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.dojo import Dojo
from pprint import pprint

@app.route("/dojos")
def dojo_display():
    dojos = Dojo.get_all()
    
    for i in range(len(dojos)):
        data = {
            'id': dojos[i].id
        }
        dojos[i] = Dojo.show_ninjas(data)
        for ninja in range(len(dojos[i].ninjas)):
            if (dojos[i].ninjas[ninja].id == None):
                dojos[i].ninjas.clear()
    
    return render_template("dojo_add.html", dojos=dojos)

@app.route("/create_dojo", methods=['POST'])
def create_dojo():
    Dojo.save(request.form)
    return redirect("/dojos")

@app.route("/dojos/<int:id>")
def dojo_show(id):
    data = {
        'id': id
    }
    dojo = Dojo.show_ninjas(data)
    return render_template("dojo_show.html", dojo=dojo)

