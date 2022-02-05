# Installation instructions
- Install python
- Create virtual env using `python -m venv env`
- Activate env on windows using `env\Scripts\activate.bat`
- Install flask: `python -m pip install Flask`

# Build instructions
### Development server:<br>
- open a cmd and run `set FLASK_APP=index`
- run `flask run`
- go to 'localhost:5000' and add routes to see the returned values

### Production (Heroku):<br>
- commit to the main branch - this should automatically deploy to the Heroku server
- visit `https://htb-vlad-backend.herokuapp.com/`
