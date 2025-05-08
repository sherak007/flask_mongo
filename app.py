from flask import Flask, request, render_template, redirect, url_for, jsonify, flash
from pymongo import MongoClient
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB Atlas connection string
client = MongoClient("mongodb+srv://humanapi:<db_password>@cluster0.fgvbqpb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['testdb']
collection = db['userdata']

# API Route
@app.route('/api')
def api():
    with open('data.json') as file:
        data = json.load(file)
    return jsonify(data)

# Form Route
@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        try:
            collection.insert_one({'name': name, 'email': email})
            return redirect(url_for('success'))
        except Exception as e:
            flash(f"Error: {str(e)}")
            return render_template('form.html')
    return render_template('form.html')

# Success Route
@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

