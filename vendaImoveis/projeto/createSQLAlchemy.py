from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:tobikon789@localhost:5432/imoveis'
db = SQLAlchemy(app)

class Proprietarios(db.Model):
   id_proprietario = db.Column(db.Integer, primary_key=True, autoincrement=True)
   nome = db.Column(db.String(255))
   dataNasc = db.Column(db.Date)
   cpf = db.Column(db.String(11), unique=True)
   rg = db.Column(db.String(9), unique=True)
   estadoCivil = db.Column(db.String(50))
   aquisicaoImovel = db.Column(db.Date)
   profissao = db.Column(db.String(100))
  #  

   def __init__(self, nome, dataNasc, cpf,rg, estadoCivil,
                aquisicaoImovel, profissao):
                self.nome = nome
                self.dataNasc = dataNasc
                self.cpf = cpf
                self.rg = rg
                self.estadoCivil = estadoCivil
                self.aquisicaoImovel = aquisicaoImovel
                self.profissao = profissao

class Bancos(db.Model):
  id_banco = db.Column(db.Integer, primary_key=True, autoincrement=True)
  nome = db.Column(db.String)

  def __init__(self, nome):
    self.nome = nome

class Clientes(db.Model):
  id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
  nome = db.Column(db.String(255))
  dataNasc = db.Column(db.Date)
  cpf = db.Column(db.String(11), unique=True)
  rg = db.Column(db.String(9), unique=True)
  estadoCivil = db.Column(db.String(50))
  profissao = db.Column(db.String(100))
  rua = db.Column(db.String(255))
  numero = db.Column(db.Integer)
  andar = db.Column(db.Integer)
  bloco = db.Column(db.String(15))
  cep = db.Column(db.String(8))
  cidade = db.Column(db.String(255))
  uf = db.Column(db.String(2))
  id_banco = db.Column(db.Integer, ForeignKey('bancos.id_banco'))

  def __init__(self, nome, dataNasc, cpf,rg, estadoCivil,
                profissao, rua, numero, andar, bloco, cep, 
                cidade, uf, id_banco):
                self.nome = nome
                self.dataNasc = dataNasc
                self.cpf = cpf
                self.rg = rg
                self.estadoCivil = estadoCivil
                self.profissao = profissao
                self.rua = rua
                self.numero = numero
                self.andar = andar
                self.bloco = bloco
                self.cep = cep
                self.cidade = cidade
                self.uf = uf
                self.id_banco = id_banco

class Despesas(db.Model):
  id_despesa = db.Column(db.Integer, primary_key=True, autoincrement=True)
  contaLuz = db.Column(db.Float)
  contaAgua = db.Column(db.Float)
  contaCondominio = db.Column(db.Float)
  propaganda = db.Column(db.Float)

  def __init__(self, contaLuz, contaAgua, contaCondominio, propaganda):
    self.contaLuz = contaLuz
    self.contaAgua = contaAgua
    self.contaCondominio = contaCondominio
    self.propaganda = propaganda

class Imoveis(db.Model):
  id_imovel = db.Column(db.Integer, primary_key=True, autoincrement=True)
  tipo = db.Column(db.String(15))
  rua = db.Column(db.String(255))
  numero = db.Column(db.Integer)
  andar = db.Column(db.Integer)
  bloco = db.Column(db.String(15))
  cep = db.Column(db.String(8))
  cidade = db.Column(db.String(255))
  uf = db.Column(db.String(2))
  valor = db.Column(db.Float)
  disponibilidade = db.Column(db.String(15))
  id_proprietario = db.Column(db.Integer, ForeignKey('proprietarios.id_proprietario'))
  id_despesa = db.Column(db.Integer, ForeignKey('despesas.id_despesa'))

  def __init__(self, tipo, rua, numero, andar, bloco, cep, cidade, uf, valor, id_proprietario, id_despesa):
                self.tipo = tipo
                self.rua = rua
                self.numero = numero
                self.andar = andar
                self.bloco = bloco
                self.cep = cep
                self.cidade = cidade
                self.uf = uf
                self.valor = valor
                self.disponibilidade = disponibilidade
                self.id_proprietario = id_proprietario
                self.id_despesa = id_despesa

class Compras(db.Model):
  id_compra = db.Column(db.Integer, primary_key=True, autoincrement=True)
  formaPagamento = db.Column(db.String(15))
  valorTotal = db.Column(db.Float)
  valorEntrada = db.Column(db.Float)
  numParcelas = db.Column(db.Integer)
  id_imovel = db.Column(db.Integer, ForeignKey('imoveis.id_imovel'))
  id_cliente = db.Column(db.Integer, ForeignKey('clientes.id_cliente'))

  def __init__(self, formaPagamento, valorTotal, valorEntrada, numParcelas, id_imovel, id_cliente):
                self.formaPagamento = formaPagamento
                self.valorTotal = valorTotal
                self.valorEntrada = valorEntrada
                self.numParcelas = numParcelas
                self.id_imovel = id_imovel
                self.id_cliente = id_cliente

db.create_all()

# listaBanco = ['Bradesco','Itau','Caixa','Nubank','Santander','Banco do Brasil','Inter']

# for banco in listaBanco:
#   bancos = Bancos(nome=banco)
#   db.session.add(bancos)
#   db.session.commit()