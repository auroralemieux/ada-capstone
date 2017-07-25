# [mybabynamebook](https://www.mybabynamebook.com)
A student capstone project by Aurora Anderson (Ada Developers Academy, Cohort 7)

## Setup and Installation on OSX

1. Create a project folder and cd into it
2. Install Python 3.5 and virtualenv
2. In your terminal, run the command "python3 -m venv myvenv" to create a virtual env (myvenv can be any name you choose)
3. Run the command "source myvenv/bin/activate" to start your virtual environment
4. Install git and pip if you don't already have them, and create a github account
5. Clone this repo into your project folder
6. Install the pip libraries from the requirements.txt file
7. Download and install chromedriver to capstone-django-project/babynamebook/ (if you plan on running any tests)
7. Set up your local database: python manage.py migrate
8. Start your local server: python manage.py runserver
9. Open the project in your browser at "http://127.0.0.1:8000/"

## Caveats

As this is a student project, and my first python/django app, period, there are some things that are a little broken! Some image links may not work locally, as they are set up to work in production. Other things may not work as they are set up to use environment variables from MY machine for authentication for AWS. TODO: Complete separation of environments for dev/prod. Also, the tests are a work in progress.
