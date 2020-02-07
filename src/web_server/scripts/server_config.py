import thread
import os, sys
from flask import Flask, render_template, request, session, redirect, escape, render_template_string, Response, send_from_directory, url_for

NODE_NAME    = "web_server"
FILE_PATH    = os.path.dirname(os.path.realpath(__file__))
PACKAGE_NAME = "mdx_brainstorm_robot_app_server"
HOST         = "0.0.0.0"
PORT         = 8000

app = Flask(__name__)
app.secret_key = os.urandom(200)