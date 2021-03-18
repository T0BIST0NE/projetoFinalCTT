CREATE TABLE Proprietarios (
    id_proprietario SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    dataNasc DATE NOT NULL,
    cpf VARCHAR(11) NOT NULL,
    rg VARCHAR(9) NOT NULL,
    estadoCivil VARCHAR(50) NOT NULL,
    aquisicaoImovel DATE NOT NULL,
    profissao VARCHAR(100) NOT NULL
);

CREATE TABLE Bancos(
    id_banco SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL
);

CREATE TABLE Clientes (
    id_cliente SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    dataNasc DATE NOT NULL,
    cpf VARCHAR(30) NOT NULL,
    rg VARCHAR(30)NOT NULL,
    estadoCivil VARCHAR(50) NOT NULL,
    profissao VARCHAR(100) NOT NULL,
    rua VARCHAR(255) NOT NULL,
    numero INTEGER NOT NULL,
    andar INTEGER,
    bloco VARCHAR(15),
    cep VARCHAR(8) NOT NULL,
    cidade VARCHAR(255) NOT NULL,
    uf VARCHAR(2) NOT NULL,
    id_banco INTEGER NOT NULL

    FOREIGN KEY (id_banco) 
    REFERENCES Bancos (id_banco)
);

CREATE TABLE Despesas(
    id_despesa SERIAL PRIMARY KEY,
    contaLuz DOUBLE NOT NULL,
    contaAgua DOUBLE NOT NULL,
    contaCondominio DOUBLE NOT NULL,
    propaganda DOUBLE NOT NULL
);

CREATE TABLE Imoveis(
    id_imovel SERIAL PRIMARY KEY,
    tipo VARCHAR(15) NOT NULL,
    rua VARCHAR(255) NOT NULL,
    numero INTEGER NOT NULL,
    andar INTEGER,
    bloco VARCHAR(15),
    cep VARCHAR(8) NOT NULL,
    cidade VARCHAR(255) NOT NULL,
    uf VARCHAR(2) NOT NULL,
    valor DOUBLE NOT NULL,
    disponibilidade VARCHAR(15) NOT NULL,
    id_proprietario INTEGER NOT NULL,
    id_despesa INTEGER NOT NULL,

    FOREIGN KEY (id_proprietario) 
    REFERENCES Proprietarios (id_proprietario),
    FOREIGN KEY (id_despesa) 
    REFERENCES Despesas(id_despesa)
);


CREATE TABLE Compras(
    id_compra SERIAL PRIMARY KEY,
    formaPagamento VARCHAR(15) NOT NULL,
    valorTotal DOUBLE NOT NULL,
    valorEntrada DOUBLE,
    numParcelas DOUBLE,
    id_imovel INTEGER NOT NULL,
    id_cliente INTEGER NOT NULL,

    FOREIGN KEY (id_imovel) 
    REFERENCES Imoveis (id_imovel),
    FOREIGN KEY (id_cliente) 
    REFERENCES Clientes(id_cliente)
);