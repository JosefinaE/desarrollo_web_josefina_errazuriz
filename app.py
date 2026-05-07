from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

app = Flask(__name__)



def getSession():
    connection_string = "mysql+pymysql://cc5002:cc5002@localhost:3306/ejemplo"
    engine = create_engine(connection_string, echo=True)
    return Session(engine)

@app.route("/")
def home():
    return "<p>Hello, World!</p>"






if __name__ == "__main__":
    # Run the app in debug mode for easier development
    app.run(debug=True)
