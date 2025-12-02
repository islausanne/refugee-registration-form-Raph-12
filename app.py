import json
import os

from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages




# Home route
@app.route('/')
def index():
   return render_template('index.html')


# Registration form page
@app.route('/register')
def register():
   return render_template('register.html')


# Handle form submission (students will add JSON save code here)
@app.route('/submit', methods=['POST'])
def submit_form():
   first_name = request.form['first_name']
   last_name = request.form['last_name']
   country = request.form['country']
   age = request.form['age']
   gender = request.form['gender']
   date_of_birth = request.form['date_of_birth']
   email = request.form['email']
   phone = request.form['phone']
   nationality = request.form['nationality']
   medical_information = request.form['medical_information']
   family_information = request.form['family_information']


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

   if not first_name or not last_name or not country or not age or not gender:
       flash('Please fill in all fields')
       return redirect(url_for('register'))

   if not country.isalpha():
        flash('Please enter a country')
        return redirect(url_for('register'))

   if not age.isnumeric():
        flash('Please enter an age')
        return redirect(url_for('register'))

   if not gender.isalpha():
        flash('Please enter a gender')
        return redirect(url_for('register'))



   # Check if file exists
   if os.path.exists('registrations.json'):
       with open('registrations.json', 'r') as file:
           data = json.load(file)
   else:
       data = []


   # Add the new registration
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
                'email': email})


   # Save all registrations back to the file
   with open('registrations.json', 'w') as file:
       json.dump(data, file, indent=2)


   return redirect(url_for('index'))


@app.route('/view')
def view_registrations():
   with open('registrations.json', 'r') as file:
       data = json.load(file)
   return render_template('view.html', registrations=data)



if __name__ == '__main__':
   app.run(debug=True)




