"""
This code programs a refugee registration form for refugees to fill out if they wish to enter the country with all essential fields.
Author : Raphael Guillon
"""

#This is where all the different python packages and services are imported.
import json
import os
import re
from flask import Flask, render_template, request, redirect, url_for, flash, session

#This allows me to run flask and the key is needed for flash messages
app = Flask(__name__)
app.secret_key = 'supersecretkey'


#This is the creation of the app route for the main page. In this main page I run the html file that I created call index.html.
@app.route('/')
def index():
   return render_template('index.html')


# This is the registration form page. This is a new route created at the top and the user can click it to access the registration form section where they will be able to fill out the form.
@app.route('/register')
def register():
   return render_template('register.html')


# This route handles the form submission(This is where the JSON save code will be), it saves all variables and appends it to a list.
@app.route('/submit', methods=['POST'])
def submit_form(regex=None):

   #This is where the variables for each of my fields are created.
   first_name = request.form['first_name']
   last_name = request.form['last_name']
   country = request.form['country']
   age = request.form['age']
   gender = request.form['gender']
   date_of_birth = request.form['date_of_birth']
   email = request.form['email']
   phone = request.form['phone']
   nationality = request.form['nationality']
   skills = request.form['skills']
   medical_information = request.form['medical_information']
   family_information = request.form['family_information']


   #This isolates each session so the variables are saved per session and reset after it starts again.
   session['first_name'] = first_name
   session['last_name'] = last_name
   session['country'] = country
   session['age'] = age
   session['gender'] = gender
   session['date_of_birth'] = date_of_birth
   session['nationality'] = nationality
   session['email'] = email
   session['phone'] = phone
   session['medical_information'] = medical_information
   session['family_information'] = family_information
   session['skills'] = skills

   #This is the validation that checks whether the first name, last name, country, age, or gender are filled or not.
   if not first_name or not last_name or not country or not age or not gender:
       flash('Please fill in all fields')
       return redirect(url_for('register'))

   #This checks that the country is written in words.
   if not country.isalpha():
        flash('Please enter a country')
        return redirect(url_for('register'))

   #This checks that the age is a number.
   if not age.isnumeric():
        flash('Please enter an age')
        return redirect(url_for('register'))

   #This checks that the gender is written in words.
   if not gender.isalpha():
        flash('Please enter a gender')
        return redirect(url_for('register'))

   email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

   #This checks that the email is written in the correct regex format.
   if not re.match(email_regex, email):
       flash('Please enter a valid email')
       return redirect(url_for('register'))




   # This checks if the file exists.
   if os.path.exists('registrations.json'):
       with open('registrations.json', 'r') as file:
           data = json.load(file)
   else:
       data = []


   # This is where the data is added to the list.
   data.append({'first_name': first_name,
                'last_name': last_name,
                'country': country,
                'age': age,
                'gender': gender,
                'date_of_birth': date_of_birth,
                'nationality' : nationality,
                'medical_information': medical_information,
                'family_information': family_information,
                'phone': phone,
                'skills': skills,
                'email': email})


   # This saves all registrations back to the file
   with open('registrations.json', 'w') as file:
       json.dump(data, file, indent=2)


   return redirect(url_for('index'))

#This sets a route to access the view page where the user is able to see all the registrations.
@app.route('/view')
def view_registrations():
   with open('registrations.json', 'r') as file:
       data = json.load(file)
   return render_template('view.html', registrations=data)



if __name__ == '__main__':
   app.run(debug=True)




