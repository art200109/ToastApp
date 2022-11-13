from flask import Flask, render_template, redirect, url_for, request

template_dir = os.path.dirname(__file__)
app = Flask(__name__, template_folder=template_dir)

# Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    return "Eyal The King"
       
if __name__ == "__main__":
    app.run(debug=True)
