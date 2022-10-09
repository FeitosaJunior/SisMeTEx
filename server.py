from flask import Flask, render_template, request, redirect, url_for, session
from forms import *
from algos.pressao import *


app = Flask(__name__)
app.secret_key = "any-string-you-want-just-keep-it-secret"


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


@app.route("/index.html", methods=["GET", "POST"])
def home2():
    return render_template("index.html")


@app.route("/meteorologia.html", methods=["GET", "POST"])
def meteorologia():
    form = InfoForm()

    if form.validate_on_submit():
        session['startdate'] = form.startdate.data
        session['enddate'] = form.enddate.data
        session['station'] = form.station.data.replace(' ', '_')
        print(session['startdate'], session['enddate'], session['station'])
        graf_pressão(session)
    return render_template("meteorologia.html", form=form)


@app.route("/generic.html")
def generic():
    return render_template("generic.html")


@app.route("/elements.html")
def elements():
    return render_template("elements.html")


"""@app.route("/pressao", methods=['GET', 'POST'])
def pressao():
    startdate = session['startdate']
    enddate = session['enddate']
    station = session['station']
    
    return render_template('pressao.html')"""


if __name__ == "__main__":
    app.run(debug=True)
