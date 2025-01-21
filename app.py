from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import pymysql
import pickle
import pandas as pd

app = Flask(__name__)

# Configuration de la base de données MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Utilisateur MySQL
app.config['MYSQL_PASSWORD'] = 'rootroot'  # Mot de passe MySQL
app.config['MYSQL_DB'] = 'customers'  # Base de données MySQL
# mysql = MySQL(app)

# Initialisation de l'extension MySQL
#mysql = MySQL(app)

methods=['POST', 'PUT', 'GET', 'PATCH', 'DELETE']

def get_db():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )


"""Récupérer touted les informations du client
    Returns:
        _type_: _description_
    """
@app.route('/', methods=['GET'])
def list_customers():
    per_page = int(request.args.get('per_page', 10))
    page = int(request.args.get('page', 1))
    offset = (page - 1) * per_page
    
    # Récupération d'une connexion à la base de données && Création d'un curseur pour exécuter des requêtes SQL
    cur = get_db().cursor()
    cur.execute(f"SELECT * FROM customers LIMIT {offset}, {per_page}")
    customers = cur.fetchall()

    # Compter le nombre total de lignes
    cur.execute("SELECT COUNT(*) as nb FROM customers")
    # total_customers = 1000 #cur.fetchone()[0]
    
    result = cur.fetchone()
    
    total_customers = 1
    if result is not None:
        total_customers = result['nb']

    total_pages = (total_customers // per_page) + (total_customers % per_page > 0)
    
    return render_template('index.html', customers=customers, page=page, per_page=per_page, total_pages=total_pages)


"""création d'un nouveau client
    Returns:
        _type_: _description_
    """
@app.route('/create_customer', methods=['GET', 'POST'])
def create_customer():
    if request.method == 'POST':
        # Handle form submission
        customer_data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'address': request.form['address'],
            'gender': request.form['gender'],
            'age': request.form['age'],
            'registered': request.form['registered'],
            'orders': request.form['orders'],
            'spent': request.form['spent'],
            'job': request.form['job'],
            'hobbies': request.form['hobbies'],
            'is_married': 'is_married' in request.form
        }
        
        sql = """ INSERT INTO customers  (first_name, last_name, email, phone, address, gender, age, registered, orders, spent, job, hobbies, is_married)
                    VALUES (%(first_name)s, %(last_name)s, %(email)s, %(phone)s, %(address)s, %(gender)s, %(age)s, %(registered)s, %(orders)s, %(spent)s, %(job)s, %(hobbies)s, %(is_married)s)
            """
        
        cur = get_db().cursor()
        
        # Exécution de la requête
        cur.execute(sql, customer_data)
        
        # mysql.connection.commit()
        cur.connection.commit()
        cur.close()
        # Do something with customer_data (e.g., save to a database)
        return redirect(url_for('create_customer'))
    return render_template('customer_create_form.html')



@app.route('/housing_list', methods=['GET'])
def housing_list():
    per_page = int(request.args.get('per_page', 10))
    page = int(request.args.get('page', 1))
    offset = (page - 1) * per_page
    
    # Récupération d'une connexion à la base de données && Création d'un curseur pour exécuter des requêtes SQL
    cur = get_db().cursor()
    cur.execute(f"SELECT * FROM california_housing LIMIT {offset}, {per_page}")
    california_housing = cur.fetchall()

    # Compter le nombre total de lignes
    cur.execute("SELECT COUNT(*) as nb FROM california_housing")
    
    result = cur.fetchone()
    
    total_california_housing = 1
    if result is not None:
        total_california_housing = result['nb']

    total_pages = (total_california_housing // per_page) + (total_california_housing % per_page > 0)
    
    return render_template('california_housing.html', california_housing=california_housing, page=page, per_page=per_page, total_pages=total_pages)



@app.route('/model', methods=['GET', 'POST'])
def modele_page(): 
    if request.method == 'POST':
        # Handle form submission
        data = {
            'MedInc': request.form['med_inc'],
            'HouseAge': request.form['house_age'],
            'AveRooms': request.form['ave_rooms'],
            'AveBedrms': request.form['ave_bed_rms'],
            'Population': request.form['population'],
            'AveOccup': request.form['ave_occupation'],
            'Latitude': request.form['latitude'],
            'Longitude': request.form['longitude']
        }
        
        # 'price': request.form['price']
        # price = request.form['price']
        
        print(data)
        
        df_mydata = pd.DataFrame.from_dict(data, orient='index').T
        
        #read the model file with PICKLE
        with open('model/price_predict.pkl', 'rb') as fichier:
            model_loader = pickle.load(fichier)
        
        # Used the model for price prediction
        price_predict = model_loader.predict(df_mydata)
        
        data['price'] = request.form['price']
        data['price_predict'] = price_predict[0]
        
        cur = get_db().cursor()
        
        if request.form.get('_method') == 'PUT':
            print(" sql update")
            id_housing = request.form['id']
            print(f""" id_housing : {id} """)
            cur.execute(""" UPDATE california_housing SET price_predict=%s WHERE id=%s """, (price_predict[0], id_housing))
            
        else:
            print(" sql insert")
            sql = """ INSERT INTO california_housing SET (med_inc, house_age, ave_rooms, ave_bed_rms, population, ave_occupation, latitude, longitude, price, price_predict)
                        VALUES (%(MedInc)s, %(HouseAge)s, %(AveRooms)s, %(AveBedrms)s, %(Population)s, %(AveOccup)s, %(Latitude)s, %(Longitude)s, %(price)s, %(price_predict)s)
                """
    
            # Exécution de la requête
            cur.execute(sql, data)
            
        
        # mysql.connection.commit()
        cur.connection.commit()
        cur.close()
        # Do something with customer_data (e.g., save to a database)
        return redirect(url_for('modele_page'))
    return render_template('model_form.html')


@app.route('/edit_customer/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    #if request.form.get('_method') == 'PUT':
    if request.method == 'POST':
        details = request.form
        first_name = details['first_name']
        last_name = details['last_name']
        email = details['email']
        phone = details['phone']
        address = details['address']
        gender = details['gender']
        age = details['age']
        registered = details['registered']
        orders = details['orders']
        spent = details['spent']
        job = details['job']
        hobbies = details['hobbies']
        is_married = 'is_married' in request.form

        cur = get_db().cursor()
        cur.execute("""
            UPDATE customers SET first_name=%s, last_name=%s, email=%s, phone=%s, address=%s, gender=%s, age=%s, registered=%s, 
                orders=%s, spent=%s, job=%s, hobbies=%s, is_married=%s
            WHERE id=%s """, 
            (first_name, last_name, email, phone, address, gender, age, registered, orders, spent, job, hobbies, is_married, customer_id))
        cur.connection.commit()
        cur.close()
        #flash('Customer Updated Successfully!')
        return redirect(url_for('edit_customer', customer_id=customer_id))
    else:
        cur = get_db().cursor()
        cur.execute("SELECT * FROM customers WHERE id=%s", (customer_id,))
        customer = cur.fetchone()
        cur.close()
        return render_template('edit_customer.html', customer=customer)


# Route pour obtenir un client par son ID (GET)
@app.route('/customer_modify/<int:id>', methods=methods)
def customer_modify(id):
    cur = get_db().cursor()
    cur.execute("SELECT * FROM customers WHERE id = %s", (id,))
    customer = cur.fetchone()
    cur.close()
    
    if customer:
        return render_template('edit_customer.html', customer=customer)
    else:
        return jsonify({'message': 'Client non trouvé'}), 404



# Route pour obtenir une client par son ID (GET)
@app.route('/customer/<int:id>', methods=methods)
def customer_detail(id):
    cur = get_db().cursor()
    cur.execute("SELECT * FROM customers WHERE id = %s", (id,))
    customer = cur.fetchone()
    cur.close()
    
    if customer:
        return render_template('customer_detail.html', customer=customer)
    else:
        return jsonify({'message': 'client non trouvée'}), 404



# Route pour supprimer une client (DELETE)
@app.route('/del_customer/<int:id>', methods=methods)
def delete_customer(id):
    if request.form.get('_method') == 'DELETE':
        cur = get_db().cursor()
        cur.execute("DELETE FROM customers WHERE id=%s", (id,))
        cur.connection.commit()
        cur.close()
    return redirect(url_for('list_customers'))

    """return the help page

    Returns:
        _type_: _description_
    """
@app.route('/help', methods=['GET'])
def help():
    return render_template('help.html')
    


# Route pour mettre à jour partiellement une client (PATCH)
@app.route('/edit_patch/<int:id>', methods=methods)
def partially_update_customer(id):
    if request.form.get('_method') == 'PATCH':
        customer = request.form.get('customer_patch')
        if customer is None:
            return jsonify({'error': 'Nouvelle client non spécifiée'}), 400
        cur = get_db().cursor()
        cur.execute("UPDATE customers SET customer=%s WHERE id=%s", (customer, id))
        cur.connection.commit()
        cur.close()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(port=5050)
