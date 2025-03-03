from flask import Flask
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object('app.config.Config')

mail = Mail(app)

from app import views