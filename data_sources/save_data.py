from flask import Flask, render_template, request, redirect, url_for
import os
from os.path import join, dirname, realpath
import pandas as pd
import pymysql

save_data = Flask(__name__)

# Configuration de la base de données MySQL
save_data.config['MYSQL_HOST'] = 'localhost'
save_data.config['MYSQL_USER'] = 'root'  # Utilisateur MySQL
save_data.config['MYSQL_PASSWORD'] = 'rootroot'  # Mot de passe MySQL
save_data.config['MYSQL_DB'] = 'customers'  # Base de données MySQL



# enable debugging mode
save_data.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = 'static'
save_data.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

methods=['POST', 'PUT', 'GET', 'PATCH', 'DELETE']

def get_db():
    return pymysql.connect(
        host=save_data.config['MYSQL_HOST'],
        user=save_data.config['MYSQL_USER'],
        password=save_data.config['MYSQL_PASSWORD'],
        db=save_data.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )


# Root URL
@save_data.route('/')
def index():
     # Set The upload HTML templates '\templates\save_data_form.html'
    return render_template('save_data_form.html')


# Get the uploaded files
@save_data.route("/", methods=['POST'])
def uploadFiles():
      # get the uploaded file
      uploaded_file = request.files['file']
      if uploaded_file.filename != '':
           file_path = os.path.join(save_data.config['UPLOAD_FOLDER'], uploaded_file.filename)
          # set the file path
           print(file_path)
           uploaded_file.save(file_path)
           #parseCSV(file_path)
           parseCSV()
          # save the file
      return redirect(url_for('index'))

def parseCSV():
      # CVS Column Names
      col_names = ['first_name', 'last_name', 'email', 'phone', 'address', 'gender', 'age', 'registered', 'orders', 'spent', 'job', 'hobbies', 'is_married']

      # Use Pandas to parse the CSV file
      csvData = pd.read_csv('data_sources/static/customers.csv')#, names=col_names, header=None
      # Loop through the Rows
      for i,row in csvData.iterrows():
             sql = "INSERT INTO customers (first_name, last_name, email, phone, address, gender, age, registered, orders, spent, job, hobbies, is_married) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
             value = (row['first_name'], row['last_name'], row['email'], row['phone'], row['address'], row['gender'], row['age'], row['registered'], row['orders'], row['spent'], row['job'], row['hobbies'], row['is_married'])
             print(value)
             cur = get_db().cursor()
             # cur.execute(sql, value, if_exists='append')
             cur.execute(sql, value)
             cur.connection.commit()
             cur.close()
             value = (row['first_name'], row['last_name'], row['email'], row['phone'], row['address'], row['gender'], row['age'], row['registered'], row['orders'], row['spent'], row['job'], row['hobbies'], row['is_married'])

if (__name__ == "__main__"):
     save_data.run(port = 8000)

