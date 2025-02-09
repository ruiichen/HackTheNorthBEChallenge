from flask import Flask
from flask_graphql import GraphQLView
from hackers.database.init_db import init_db
from .database.db_session import db_session
from .schema.schema import schema

app = Flask(__name__)
app.debug = True

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)

@app.before_first_request
def initialize_database():
    init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()