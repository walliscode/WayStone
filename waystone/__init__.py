from flask import Flask

app = Flask(__name__) # create the application instance


@app.route('/') # using the route() decorator to tell Flask what URL should trigger our function, in this case the root URL /
def hello():
    return 'Hello, World!'

