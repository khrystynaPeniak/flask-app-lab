from flask import Flask, request, redirect,  url_for
app = Flask(__name__)

@app.route('/')
def main():
    return "Hello, world!"

@app.route('/homepage') 
def home():
    """View for the Home page of your website."""
    agent = request.user_agent
    return f"<h1>This is your homepage :) - {agent}</h1>"

@app.route('/hi/<string:name>')  
def greeting(name):
    name = name.upper()
    age = request.args.get("age", 0, type=int)
    #year = 2024 - age
    return f"Welcome {name=} {age=}", 200

@app.route('/admin')
def admin():
    to_url = url_for("greeting", name="administrator", _external=True) 
    print(to_url)
    return redirect(to_url)

if __name__ == '__main__':
    app.run(debug=True)