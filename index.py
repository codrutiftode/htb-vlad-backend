from flask import Flask


app = Flask(__name__)

@app.route('/api/hello')
def api():
    return "Hey"

# @app.route('/api')
# def api():
#     with open('data.json', mode='r') as my_file:
#         text = my_file.read()
#         return text

@app.route('/')
def home():
    return 'Home Page Route'


@app.route('/about')
def about():
    return 'About Page Route'


@app.route('/portfolio')
def portfolio():
    return 'Portfolio Page Route'


@app.route('/contact')
def contact():
    return 'Contact Page Route'

# Run the application
if __name__ == '__main__':
    app.run()