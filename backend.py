from flask import Flask, render_template, request, jsonify, redirect, url_for
import pymysql

backend = Flask(__name__)

# Configuration de la base de données MySQL
backend.config['MYSQL_HOST'] = 'localhost'
backend.config['MYSQL_USER'] = 'root'  # Utilisateur MySQL
backend.config['MYSQL_PASSWORD'] = 'rootroot'  # Mot de passe MySQL
backend.config['MYSQL_DB'] = 'customers'  # Base de données MySQL

methods=['POST', 'PUT', 'GET', 'PATCH', 'DELETE']

def get_db():
    return pymysql.connect(
        host=backend.config['MYSQL_HOST'],
        user=backend.config['MYSQL_USER'],
        password=backend.config['MYSQL_PASSWORD'],
        db=backend.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )

@backend.route('/index')
def index():
    # Récupération d'une connexion à la base de données && Création d'un curseur pour exécuter des requêtes SQL
    cur = get_db().cursor()
    cur.execute("SELECT * FROM reportings")
    cur.connection.commit()
    reportings = cur.fetchall()
    cur.close()
    #return render_template('index.html', reportings=reportings)
    return jsonify(reportings)

# Route pour obtenir une tâche par son ID (GET)
@backend.route('/data/<int:id>', methods=methods)
def get_task(id):
    cur = get_db().cursor()
    cur.execute("SELECT * FROM reportings WHERE id = %s", (id,))
    reporting = cur.fetchone()
    cur.close()
    if reporting:
        # return render_template('index.html', reporting=reporting)
        return jsonify(reporting)
    else:
        return jsonify({'message': 'Tâche non trouvée'}), 404
    
# Route pour mettre à jour une tâche (PUT)
@backend.route('/edit_data/<int:id>', methods=methods)
def update_task(id):
    if request.form.get('_method') == 'PUT':
        task = request.form.get('new_task')
        if task is None:
            return jsonify({'error': 'Nouvelle maj non spécifiée'}), 400
        cur = get_db().cursor()
        cur.execute("UPDATE tasks SET task=%s WHERE id=%s", (task, id))
        cur.connection.commit()
        cur.close()
    #return jsonify({'error': 'Tache non trouvee'}), 404  # Retourner une réponse JSON d'erreur si la tâche n'est pas trouvée
    return jsonify({'message': 'La mise à jour a été effectuée avec succès'}), 200

# Route pour supprimer une tâche (DELETE)
@backend.route('/del_data/<int:id>', methods=methods)
def delete_task(id):
    if request.form.get('_method') == 'DELETE':
        cur = get_db().cursor()
        cur.execute("DELETE FROM tasks WHERE id=%s", (id,))
        cur.connection.commit()
        cur.close()
    return jsonify({'message': f"""La suppression de l'id ${id} a été effectuée avec succès"""}), 200

# Route pour mettre à jour partiellement une tâche (PATCH)
@backend.route('/edit_data/<int:id>', methods=methods)
def partially_update_task(id):
    if request.form.get('_method') == 'PATCH':
        task = request.form.get('task_patch')
        if task is None:
            return jsonify({'error': 'Nouvelle tâche non spécifiée'}), 400
        cur = get_db().cursor()
        cur.execute("UPDATE tasks SET task=%s WHERE id=%s", (task, id))
        cur.connection.commit()
        cur.close()
    return jsonify({'message': 'La mise à jour partielle a été effectuée avec succès'}), 200



if __name__ == '__main__':
    backend.run(debug=True)
