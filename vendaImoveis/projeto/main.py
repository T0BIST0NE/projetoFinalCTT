from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from createSQLAlchemy import Imoveis, Proprietarios, Clientes, Compras

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:tobikon789@localhost:5432/imoveis'
db = SQLAlchemy(app)

@app.route('/')
def index():
  return render_template('index.html', clientes = Clientes.query.all())

if __name__ == '__main__':
    app.run(debug=True)