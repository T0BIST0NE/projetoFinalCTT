from flask import Flask, request, jsonify
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from flask_cors import CORS

app = Flask(__name__)
app_ = Api(app = app, 
		  version = "1.0", 
		  title = "Venda de Imóveis", 
		  description = "Sistema de venda de imóveis")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:tobikon789@localhost:5432/imoveis'
app.config['SECRET_KEY'] = "tbkn789"
app.debug = True
CORS(app)
db = SQLAlchemy(app)

prop = app_.namespace('proprietarios', description='Proprietarios')
ban = app_.namespace('bancos', description='Bancos')
cl = app_.namespace('clientes', description='Clientes')
desp = app_.namespace('despesas', description='Despesas')
imv = app_.namespace('imoveis', description='Imoveis')
cmps = app_.namespace('compras', description='Compras')

#Classes com definição de atributos
class Proprietarios(db.Model):
   id_proprietario = db.Column(db.Integer, primary_key=True, autoincrement=True)
   nome = db.Column(db.String(255))
   dataNasc = db.Column(db.Date)
   cpf = db.Column(db.String(11), unique=True)
   rg = db.Column(db.String(9), unique=True)
   estadoCivil = db.Column(db.String(50))
   aquisicaoImovel = db.Column(db.Date)
   profissao = db.Column(db.String(100))
    
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

  def __init__(self, tipo, rua, numero, andar, bloco, cep, cidade, uf, valor, disponibilidade, id_proprietario, id_despesa):
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

#Modelo de Proprietarios
modelProp = app_.model('Modelo de Proprietario',{
                        'nome':fields.String(required=True,
                         description='Nome do proprietario',
                         help="Nome não pode ser nulo"),
                         'dataNasc':fields.Date(required=True,
                         description='Data de nascimento do proprietario',
                         help="Data de nascimento não pode ser nulo"),
                        'cpf':fields.String(required = True, 
    					  				 description="CPF do proprietario", 
    					  				 help="CPF não pode ser nulo."),
                         'rg':fields.String(required=True,
                         description='RG do proprietario',
                         help="RG não pode ser nulo"),
                         'estadoCivil':fields.String(required=True,
                         description='Estado civil do proprietario',
                         help="Estado civil não pode ser nulo"),
                         'aquisicaoImovel':fields.Date(required=True,
                         description='Profissao do cliente',
                         help="Data de aquisição do imóvel não pode ser nula"),
                         'profissao':fields.String(required=True,
                         description='Profissao do proprietario',
                         help="Profissao não pode ser nulo")})

modelProp_PUT = app_.model('Modelo de Proprietario',{
                        'nome':fields.String(description='Nome do proprietario'),
                         'dataNasc':fields.Date(description='Data de nascimento do proprietario'),
                        'cpf':fields.String(description="CPF do proprietario"),
                         'rg':fields.String(description='RG do proprietario'),
                         'estadoCivil':fields.String(description='Estado civil do proprietario'),
                         'aquisicaoImovel':fields.Date(description='Profissao do cliente'),
                         'profissao':fields.String(description='Profissao do proprietario')})

#Modelo de Bancos
modelBan = app_.model('Modelo de Bancos',{
                        'nome':fields.String(required=True,
                         description='Nome do banco',
                         help="Nome do banco não pode ser nulo")})

#Modelo de Clientes
modelCl = app_.model('Modelo de Clientes', {
                        'nome':fields.String(required=True,
                         description='Nome do cliente',
                         help="Nome não pode ser nulo"),
                         'dataNasc':fields.Date(required=True,
                         description='Data de nascimento do cliente',
                         help="Data de nascimento não pode ser nulo"),
                        'cpf':fields.String(required = True, 
    					  				 description="CPF do cliente", 
    					  				 help="CPF não pode ser nulo."),
                         'rg':fields.String(required=True,
                         description='RG do cliente',
                         help="RG não pode ser nulo"),
                         'estadoCivil':fields.String(required=True,
                         description='Estado civil do cliente',
                         help="Estado civil não pode ser nulo"),
                         'profissao':fields.String(required=True,
                         description='Profissao do cliente',
                         help="Profissao não pode ser nulo"),
                         'rua':fields.String(required=True,
                         description='Rua do endereço do cliente',
                         help="Nome não pode ser nulo"),
                         'numero':fields.Integer(required=True,
                         description='Número do endereço do cliente',
                         help="Nome não pode ser nulo"),
                         'andar':fields.Integer(
                         description='Andar do apartamento do cliente'),
                         'bloco':fields.Integer(
                         description='Andar do apartamento do cliente'),
                         'cep':fields.Integer(required=True,
                         description='CEP do endereço do cliente',
                         help="CEP não pode ser nulo"),
                         'cidade':fields.String(required=True,
                         description='Cidade na qual o cliente vive',
                         help="Cidade não pode ser nulo"),
                         'uf':fields.String(required=True,
                         description='Estado na qual o cliente vive',
                         help="UF não pode ser nulo"),
                         'id_banco':fields.Integer(required=True,
                         description='ID do banco na qual o cliente possui conta',
                         help="ID do banco não pode ser nulo")
                         })

modelCl_PUT = app_.model('Modelo de Clientes', {
                        'nome':fields.String(description='Nome do cliente'),
                         'dataNasc':fields.Date(description='Data de nascimento do cliente'),
                        'cpf':fields.String(description="CPF do cliente"),
                         'rg':fields.String(description='RG do cliente'),
                         'estadoCivil':fields.String(description='Estado civil do cliente'),
                         'profissao':fields.String(description='Profissao do cliente'),
                         'rua':fields.String(description='Rua do endereço do cliente'),
                         'numero':fields.Integer(description='Número do endereço do cliente'),
                         'andar':fields.Integer(description='Andar do apartamento do cliente'),
                         'bloco':fields.Integer(description='Andar do apartamento do cliente'),
                         'cep':fields.Integer(description='CEP do endereço do cliente'),
                         'cidade':fields.String(description='Cidade na qual o cliente vive'),
                         'uf':fields.String(description='Estado na qual o cliente vive'),
                         'id_banco':fields.Integer(description='ID do banco na qual o cliente possui conta')
                         })

#Modelo de Despesas
modelDesp = app_.model('Modelo de Despesas',{
                        'contaLuz':fields.Float(required=True,
                         description='Conta de luz do imovel',
                         help="Conta de luz não pode ser nula"),
                         'contaAgua':fields.Float(required=True,
                         description='Conta de água do imovel',
                         help="Conta de água não pode ser nula"),
                        'contaCondominio':fields.Float(required = True, 
    					  				 description='Conta de condominio do imovel',
                         help="Conta de condominio não pode ser nula"),
                         'propaganda':fields.Float(required=True,
                         description='Gastos com propaganda do imovel',
                         help="Gastos com propaganda não podem ser nulos")})

modelDesp_PUT = app_.model('Modelo de Despesas',{
                        'contaLuz':fields.Float(description='Conta de luz do imovel'),
                         'contaAgua':fields.Float(description='Conta de água do imovel'),
                        'contaCondominio':fields.Float(description='Conta de condominio do imovel'),
                         'propaganda':fields.Float(description='Gastos com propaganda do imovel')})

#Modelo de Imoveis
modelImov = app_.model('Modelo de Imoveis',{
                        'tipo':fields.String(required=True,
                        description='Tipo de pagamento escolhido',
                        help="O tipo do pagamento não pode ser nulo"),
                        'rua':fields.String(required=True,
                        description='Rua do imóvell',
                        help="Rua do imóvel não pode ser nula"),
                        'numero':fields.Integer(required=True,
                        description='Número do imovel',
                        help="Número do imóvel não pode ser nulo"),
                        'andar':fields.Integer(
                        description='Conta de luz do imovel'),
                        'bloco':fields.String(
                        description='Conta de luz do imovel'),
                        'cep':fields.String(required=True,
                        description='CEP do imovel',
                        help="CEP do imóvel não pode ser nulo"),
                        'cidade':fields.String(required=True,
                        description='Cidade onde se encontra o imovel',
                        help="Cidade do imóvel não pode ser nula"),
                        'uf':fields.String(required=True,
                        description='Estado onde se encontra o imovel',
                        help="Estado do imóvel não pode ser nula"),
                        'valor':fields.Float(required=True,
                        description='Valor do imovel',
                        help="Valor do imóvel não pode ser nula"),
                        'disponibilidade':fields.String(required=True,
                        description='O imovel esta disponivel para compra?',
                        help='Deve haver a disponibilidade para a venda do imovel'),
                        'id_proprietario':fields.Integer(required=True,
                        description='ID do proprietário do imovel',
                        help="ID do proprietário do imóvel não pode ser nulo"),
                        'id_despesa':fields.Integer(required=True,
                        description='ID das despesas do imovel',
                        help="ID das despesas do imóvel não pode ser nulo")})

modelImov_PUT = app_.model('Modelo de Imoveis',{
                        'tipo':fields.String(description='Tipo de pagamento escolhido'),
                        'rua':fields.String(description='Rua do imóvell'),
                        'numero':fields.Integer(description='Número do imovel'),
                        'andar':fields.Integer(description='Conta de luz do imovel'),
                        'bloco':fields.String(description='Conta de luz do imovel'),
                        'cep':fields.String(description='CEP do imovel'),
                        'cidade':fields.String(description='Cidade onde se encontra o imovel'),
                        'uf':fields.String(description='Estado onde se encontra o imovel'),
                        'valor':fields.Float(description='Valor do imovel'),
                        'disponibilidade':fields.String(description='O imovel esta disponivel para compra?'),
                        'id_proprietario':fields.Integer(description='ID do proprietário do imovel'),
                        'id_despesa':fields.Integer(description='ID das despesas do imovel')})

#Modelo de Compras
modelComp = app_.model('Modelo de Compras',{
                      'formaPagamento':fields.String(required=True,
                      description='Forma de pagamento escolhido',
                      help="A forma do pagamento não pode ser nula"),
                      'valorTotal':fields.Float(required=True,
                      description='Valor da compra do imóvel',
                      help="Valor da compra do imóvel não pode ser nulo"),
                      'valorEntrada':fields.Float(
                      description='Valor de entrada no pagamento do imovel'),
                      'numParcelas':fields.Integer(
                      description='Número de parelas de pagamento do imovel'),
                      'id_imovel':fields.Integer(required=True,
                      description='ID do imovel',
                      help="ID do imovel não pode ser nulo"),
                      'id_cliente':fields.Integer(required=True,
                      description='ID do cliente comprador do imovel',
                      help="ID do cliente comprador do imóvel não pode ser nulo")})

modelComp_PUT = app_.model('Modelo de Compras',{
                      'formaPagamento':fields.String(description='Forma de pagamento escolhido'),
                      'valorTotal':fields.Float(description='Valor da compra do imóvel'),
                      'valorEntrada':fields.Float(description='Valor de entrada no pagamento do imovel'),
                      'numParcelas':fields.Integer(description='Número de parelas de pagamento do imovel'),
                      'id_imovel':fields.Integer(description='ID do imovel'),
                      'id_cliente':fields.Integer(description='ID do cliente comprador do imovel')})

#Métodos POST, GET, DELETE e PUT de PROPRIETARIOS
@prop.route("/proprietarios")
class MainClass(Resource):
  def get(self):
      allProprietarios = Proprietarios.query.all()
      saida=[]
      for proprietario in allProprietarios:
        currProprietarios ={}
        currProprietarios['id_proprietario'] = proprietario.id_proprietario
        currProprietarios['nome'] = proprietario.nome
        currProprietarios['dataNasc'] = proprietario.dataNasc
        currProprietarios['cpf'] = proprietario.cpf
        currProprietarios['rg'] = proprietario.rg
        currProprietarios['estadoCivil'] = proprietario.estadoCivil
        currProprietarios['aquisicaoImovel'] = proprietario.aquisicaoImovel
        currProprietarios['profissao'] = proprietario.profissao
        saida.append(currProprietarios)
      return jsonify(saida)

  @app_.expect(modelProp)
  def post(self):
        dadosProprietario = request.get_json()
        pr = Proprietarios(nome=dadosProprietario['nome'],dataNasc=dadosProprietario['dataNasc'],cpf=dadosProprietario['cpf'],
                            rg=dadosProprietario['rg'],estadoCivil=dadosProprietario['estadoCivil'],aquisicaoImovel=dadosProprietario['aquisicaoImovel'],
                            profissao=dadosProprietario['profissao'])
        db.session.add(pr)
        db.session.commit()
        return jsonify(dadosProprietario)
  
@prop.route("/proprietarios/<int:id_proprietario>")
@app_.doc(params={'id_proprietario':'ID referente ao proprietario que deseja excluir'})
class MainClass(Resource):
  def delete(self, id_proprietario):
    dado_prop = Proprietarios.query.filter(Proprietarios.id_proprietario == id_proprietario).delete()
    db.session.commit()
    return jsonify(dado_prop)

@prop.route("/proprietarios/update/<int:id_proprietario>")
@app_.expect(modelProp_PUT)
class MainClass(Resource):
  def put(self, id_proprietario):
    prop_put = Proprietarios.query.get(id_proprietario)
    prop_put.nome = request.json.get('nome', prop_put.nome)
    prop_put.dataNasc = request.json.get('dataNasc', prop_put.dataNasc)
    prop_put.cpf = request.json.get('cpf', prop_put.cpf)
    prop_put.rg = request.json.get('rg', prop_put.rg)
    prop_put.estadoCivil = request.json.get('estadoCivil', prop_put.estadoCivil)
    prop_put.aquisicaoImovel = request.json.get('aquisicaoImovel', prop_put.aquisicaoImovel)
    prop_put.profissao = request.json.get('profissao', prop_put.profissao)
    db.session.commit()
    return jsonify({'nome':prop_put.nome,'dataNasc': prop_put.dataNasc,'cpf':prop_put.cpf,
                    'rg':prop_put.rg,'estadoCivil':prop_put.estadoCivil,'aquisicaoImovel':prop_put.estadoCivil,
                    'profissao':prop_put.profissao})

#Método GET e PUT de BANCOS
@ban.route("/bancos")
class MainClass(Resource):
  def get(self):
    allBancos = Bancos.query.all()
    saida=[]
    for banco in allBancos:
      currBancos ={}
      currBancos['id_banco'] = banco.id_banco
      currBancos['nome'] = banco.nome
      saida.append(currBancos)
    return jsonify(saida)

@ban.route("/bancos/update/<int:id_banco>")
@app_.expect(modelBan)
class MainClass(Resource):
  def put(self, id_proprietario):
    ban_put = Bancos.query.get(id_banco)
    ban_put.nome = request.json.get('nome', ban_put.nome)
    db.session.commit()
    return jsonify({'nome':ban_put.nome})

#Métodos POST, GET, DELETE e PUT de CLIENTES
@cl.route("/clientes")
class MainClass(Resource):
  def get(self):
      allClientes = Clientes.query.all()
      saida=[]
      for cliente in allClientes:
        currClientes ={}
        currClientes['id_cliente'] = cliente.id_cliente
        currClientes['nome'] = cliente.nome
        currClientes['dataNasc'] = cliente.dataNasc
        currClientes['cpf'] = cliente.cpf
        currClientes['rg'] = cliente.rg
        currClientes['estadoCivil'] = cliente.estadoCivil
        currClientes['profissao'] = cliente.profissao
        currClientes['rua'] = cliente.rua
        currClientes['numero'] = cliente.numero
        currClientes['andar'] = cliente.andar
        currClientes['bloco'] = cliente.bloco
        currClientes['cep'] = cliente.cep
        currClientes['cidade'] = cliente.cidade
        currClientes['uf'] = cliente.uf
        currClientes['id_banco'] = cliente.id_banco
        
        saida.append(currClientes)
      return jsonify(saida)
  
  @app_.expect(modelCl)	
  def post(self):
        dadosCliente = request.get_json()
        cli = Clientes(nome=dadosCliente['nome'],dataNasc=dadosCliente['dataNasc'],cpf=dadosCliente['cpf'],
                        rg=dadosCliente['rg'],estadoCivil=dadosCliente['estadoCivil'],profissao=dadosCliente['profissao'],
                        rua=dadosCliente['rua'],numero=dadosCliente['numero'],andar=dadosCliente['andar'],bloco=dadosCliente['bloco'],
                        cep=dadosCliente['cep'],cidade=dadosCliente['cidade'],uf=dadosCliente['uf'],id_banco=dadosCliente['id_banco'])
        db.session.add(cli)
        db.session.commit()
        return jsonify(dadosCliente)

@cl.route("/clientes/<int:id_cliente>")
@app_.doc(params={'id_cliente':'ID referente ao cliente que deseja excluir'})
class MainClass(Resource):
  def delete(self, id_cliente):
    dado_cli = Clientes.query.filter(Clientes.id_cliente == id_cliente).delete()
    db.session.commit()
    return jsonify(dado_cli)

@cl.route("/clientes/update/<int:id_cliente>")
@app_.expect(modelCl_PUT)
class MainClass(Resource):
  def put(self, id_cliente):
    cl_put = Clientes.query.get(id_cliente)
    cl_put.nome = request.json.get('nome', cl_put.nome)
    cl_put.dataNasc = request.json.get('dataNasc', cl_put.dataNasc)
    cl_put.cpf = request.json.get('cpf', cl_put.cpf)
    cl_put.rg = request.json.get('rg', cl_put.rg)
    cl_put.estadoCivil = request.json.get('estadoCivil', cl_put.estadoCivil)
    cl_put.profissao = request.json.get('profissao', cl_put.profissao)
    cl_put.rua = request.json.get('rua', cl_put.rua)
    cl_put.numero = request.json.get('numero', cl_put.numero)
    cl_put.andar = request.json.get('andar', cl_put.andar)
    cl_put.bloco = request.json.get('bloco', cl_put.bloco)
    cl_put.cep = request.json.get('cep', cl_put.cep)
    cl_put.cidade = request.json.get('cidade', cl_put.cidade)
    cl_put.uf = request.json.get('uf', cl_put.uf)
    cl_put.id_banco = request.json.get('id_banco', cl_put.id_banco)
    db.session.commit()
    return jsonify({'nome':cl_put.nome,'dataNasc': cl_put.dataNasc,'cpf':cl_put.cpf,
                    'rg':cl_put.rg,'estadoCivil':cl_put.estadoCivil,'aquisicaoImovel':cl_put.estadoCivil,
                    'profissao':cl_put.profissao,'rua':cl_put.rua,'numero':cl_put.numero,'andar':cl_put.andar,
                    'cep':cl_put.cep,'cidade':cl_put.cidade,'uf':cl_put.uf,'id_banco':cl_put.id_banco})

#Métodos POST, GET, DELETE e PUT de DESPESAS
@desp.route("/despesas")
class MainClass(Resource):
  def get(self):
      allDespesas = Despesas.query.all()
      saida=[]
      for despesa in allDespesas:
        currDespesas ={}
        currDespesas['id_despesa'] = despesa.id_despesa
        currDespesas['contaLuz'] = despesa.contaLuz
        currDespesas['contaAgua'] = despesa.contaAgua
        currDespesas['contaCondominio'] = despesa.contaCondominio
        currDespesas['propaganda'] = despesa.propaganda
        saida.append(currDespesas)
      return jsonify(saida)

  @app_.expect(modelDesp)
  def post(self):
        dadosDespesa = request.get_json()
        des = Despesas(contaLuz=dadosDespesa['contaLuz'],contaAgua=dadosDespesa['contaLuz'],contaCondominio=dadosDespesa['contaCondominio'],
                            propaganda=dadosDespesa['propaganda'])
        db.session.add(des)
        db.session.commit()
        return jsonify(dadosDespesa)

@desp.route("/despesas/<int:id_despesa>")
@app_.doc(params={'id_despesa':'ID referente as despesas que deseja excluir'})
class MainClass(Resource):
  def delete(self, id_despesa):
    dado_desp = Despesas.query.filter(Despesas.id_despesa == id_despesa).delete()
    db.session.commit()
    return jsonify(dado_desp)

@desp.route("/proprietarios/update/<int:id_despesa>")
@app_.expect(modelDesp_PUT)
class MainClass(Resource):
  def put(self, id_despesa):
    desp_put = Despesas.query.get(id_despesa)
    desp_put.contaLuz = request.json.get('contaLuz', desp_put.contaLuz)
    desp_put.contaAgua = request.json.get('contaAgua', desp_put.contaAgua)
    desp_put.contaCondominio = request.json.get('contaCondominio', desp_put.contaCondominio)
    desp_put.propaganda = request.json.get('propaganda', desp_put.propaganda)
    db.session.commit()
    return jsonify({'contaLuz':desp_put.contaLuz,'contaAgua': desp_put.contaAgua,'contaCondominio':desp_put.contaCondominio,
                    'propaganda':desp_put.propaganda})

#Métodos POST, GET, DELETE e PUT de IMOVEIS
@imv.route("/imoveis")
class MainClass(Resource):
  def get(self):
      allImoveis = Imoveis.query.all()
      saida=[]
      for imovel in allImoveis:
        currImoveis ={}
        currImoveis['id_imovel'] = imovel.id_imovel
        currImoveis['tipo'] =imovel.tipo
        currImoveis['rua'] =imovel.rua
        currImoveis['numero'] =imovel.numero
        currImoveis['andar'] =imovel.andar
        currImoveis['bloco'] =imovel.bloco
        currImoveis['cep'] =imovel.cep
        currImoveis['cidade'] =imovel.cidade
        currImoveis['uf'] =imovel.uf
        currImoveis['valor'] =imovel.valor
        currImoveis['dispinibilidade'] = imovel.disponibilidade
        currImoveis['id_proprietario'] =imovel.id_proprietario
        currImoveis['id_despesa'] =imovel.id_despesa
        saida.append(currImoveis)
      return jsonify(saida)
  
  @app_.expect(modelImov)
  def post(self):
    dadosImovel = request.get_json()
    imo = Imoveis(tipo=dadosImovel['tipo'],rua=dadosImovel['rua'],numero=dadosImovel['numero'],
                  andar=dadosImovel['andar'],bloco=dadosImovel['bloco'],cep=dadosImovel['cep'],
                  cidade=dadosImovel['cidade'],uf=dadosImovel['uf'],valor=dadosImovel['valor'],
                  disponibilidade=dadosImovel['disponibilidade'],id_proprietario=dadosImovel['id_proprietario'],
                  id_despesa=dadosImovel['id_despesa'])
    db.session.add(imo)
    db.session.commit()
    return jsonify(dadosImovel)

@imv.route("/imoveis/<int:id_imovel>")
@app_.doc(params={'id_imovel':'ID referente ao imovel que deseja excluir'})
class MainClass(Resource):
  def delete(self, id_imovel):
    dado_imv = Imoveis.query.filter(Imoveis.id_imovel == id_imovel).delete()
    db.session.commit()
    return jsonify(dado_imv)

@imv.route("/proprietarios/update/<int:id_imovel>")
@app_.expect(modelImov_PUT)
class MainClass(Resource):
  def put(self, id_imovel):
    imv_put = Imoveis.query.get(id_imovel)
    imv_put.tipo = request.json.get('tipo', imv_put.tipo)
    imv_put.rua = request.json.get('rua', imv_put.rua)
    imv_put.numero = request.json.get('numero', imv_put.numero)
    imv_put.andar = request.json.get('andar', imv_put.andar)
    imv_put.bloco = request.json.get('bloco', imv_put.bloco)
    imv_put.cep = request.json.get('cep', imv_put.cep)
    imv_put.cidade = request.json.get('cidade', imv_put.cidade)
    imv_put.uf = request.json.get('uf', imv_put.uf)
    imv_put.valor = request.json.get('valor', imv_put.valor)
    imv_put.disponibilidade = request.json.get('disponibilidade', imv_put.disponibilidade)
    imv_put.id_proprietario = request.json.get('id_proprietario', imv_put.id_proprietario)
    imv_put.id_despesa = request.json.get('id_despesa', imv_put.id_despesa)
    db.session.commit()
    return jsonify({'tipo':imv_put.tipo,'rua': imv_put.rua,'numero':imv_put.numero,
                    'andar':imv_put.andar,'bloco':imv_put.bloco,'cep':imv_put.cep,
                    'cidade':imv_put.cidade,'uf':imv_put.uf,'valor':imv_put.valor,
                    'disponibilidade':imv_put.disponibilidade,'id_proprietario':imv_put.id_proprietario,
                    'id_despesa':imv_put.id_despesa})

#Métodos POST, GET e PUT de COMPRAS
@cmps.route("/compras")
class MainClass(Resource):
  def get(self):
      allCompras = Compras.query.all()
      saida=[]
      for compra in allCompras:
        currCompras ={}
        currCompras['id_compra'] = compra.id_compra
        currCompras['formaPagamento'] = compra.formaPagamento
        currCompras['valorTotal'] = compra.valorTotal
        currCompras['valorEntrada'] = compra.valorEntrada
        currCompras['numParcelas'] = compra.numParcelas
        currCompras['id_imovel'] = compra.id_imovel
        currCompras['id_cliente'] = compra.id_cliente
        saida.append(currCompras)
      return jsonify(saida)
  
  @app_.expect(modelComp)
  def post(self):
    dadosCompra = request.get_json()
    cm = Compras(formaPagamento=dadosCompra['formaPagamento'],valorTotal=dadosCompra['valorTotal'],valorEntrada=dadosCompra['valorEntrada'],
                  numParcelas=dadosCompra['numParcelas'],id_imovel=dadosCompra['id_imovel'],id_cliente=dadosCompra['id_cliente'])
    db.session.add(cm)
    db.session.commit()
    return jsonify(dadosCompra)

@cmps.route("/proprietarios/update/<int:id_compra>")
@app_.expect(modelComp_PUT)
class MainClass(Resource):
  def put(self, id_compra):
    cmp_put = Compras.query.get(id_compra)
    cmp_put.formaPagamento = request.json.get('formaPagamento', cmp_put.formaPagamento)
    cmp_put.valorTotal = request.json.get('valorTotal', cmp_put.valorTotal)
    cmp_put.valorEntrada = request.json.get('valorEntrada', cmp_put.valorEntrada)
    cmp_put.numParcelas = request.json.get('numParcelas', cmp_put.numParcelas)
    cmp_put.id_imovel = request.json.get('id_imovel', cmp_put.id_imovel)
    cmp_put.id_cliente = request.json.get('id_cliente', cmp_put.id_cliente)
    db.session.commit()
    return jsonify({'formaPagamento':cmp_put.formaPagamento,'valorTotal': cmp_put.valorTotal,'valorEntrada':cmp_put.valorEntrada,
                    'numParcelas':cmp_put.numParcelas,'id_imovel':cmp_put.id_imovel,'id_cliente':cmp_put.id_cliente})