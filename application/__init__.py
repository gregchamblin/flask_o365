from flask import Flask

app = Flask(__name__)
app.secret_key = "mo\xf9\x83W\xc1\xb0\xd48\xd8\xca\t\x02.J\x05"

from application import routes

