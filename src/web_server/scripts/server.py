import os, sys
sys.path.insert(0,os.path.dirname(os.path.realpath(__file__)))
import matplotlib.pyplot as plt
import time
import random
from server_config import *

should_activate_experiment = False

def __log(status="INFO", message=""):
    print("[{status}] {message}".format(status=status, message=message))

    ## logging
    # app.logger.debug("Logging debug messages")
    # app.logger.warning("Logging warnings")
    # app.logger.error("Logging erros")

@app.route("/")
def index():
    return render_template("index.html", logged_in=False)


@app.route("/rosbridge")
def rosbridge():
    return render_template("rosbridge.html", logged_in=False)

@app.route("/plot")
def plot():
    left = [1, 2, 3, 4, 5]
    height = [10, 24, 36, 40, 5]
    tick_label = ['one', 'two', 'three', 'four', 'five']
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['red', 'green'])
    plt.ylabel('y - axis')
    plt.xlabel('x - axis')
    plt.title('Eurobot bar chart')
    plt.savefig('/static/img/plot.png')
    return render_template("plot.html", url='../static/img/plot.png')


@app.route("/urdf")
def urdf():
    return render_template("urdf.html", logged_in=False)



@app.route("/test")
def test():
    return "Test Successful"

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    uname = request.form["username"]
    key   = request.form["password"]

    # if uname in session:
    #     return "Logged in as {uname}".format(uname=uname)

    # session["username"] = uname

    if request.method == "POST":
        return "LOGIN VIA POST"
    else:
        return "LOGIN VIA GET"

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

@app.route("/shutdown_server")
@app.route("/kill_server")
def shutdown_server():
    __log("Shutting down the server ...")

    try:
        thread.exit()
    except:
        __log("Failed to exit server thread ...")

    # sys.exit(0)