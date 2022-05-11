
from flask import Flask, render_template, request, redirect, session, flash, url_for
import pFuncoes as f
import pandas as pd

app = Flask(__name__)
app.secret_key = 'EasyManager'

def autenticaUsuario(lista):
    usuario = lista[0]
    return usuario[0]


def separaUser(lista):
    df = pd.DataFrame(lista, columns=["id", "usuario","nivel_acesso"])
    tamanho = len(df)
    id_usuario = []
    usuario = []
    nivel_acesso = []
    for i in range(0, tamanho):
        id_usuario.append(df['id'][i])
        usuario.append(df['usuario'][i])
        nivel_acesso.append(df['nivel_acesso'][i])

    return id_usuario, usuario, nivel_acesso

def ultimoID(lista):
    df = pd.DataFrame(lista, columns=["id"])
    tamanho = len(df)
    id_usuario = []
   
    for i in range(0, tamanho):
        id_usuario.append(df['id'][i])
        
    return id_usuario

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == "GET":
        session['usuario'] = None
        return render_template('Login.html')
    else:
        usuario = request.form['usuario']
        senha = request.form['senha']
        SQL_AUTENTICAR = "SELECT usuario, senha, nivel_acesso from users where usuario = '{0}' and senha = '{1}'".format(usuario, senha)
        select = f.consulta_bd(SQL_AUTENTICAR)
        
        if select != []:
            
            usu = autenticaUsuario(select)
            session['usuario'] = usu
            return redirect(url_for('index'))
        else:
            flash('Acesso negado! Usuário ou senha não coincidem.')
            return render_template('Login.html')

@app.route('/novo_usuario')
def novo_usuario():
    #if 'usuario_logado' not in session or session['usuario_logado'] == None:
    #    return redirect(url_for('login'))
    return render_template('Novo_Usuario.html', titulo='Formulário de Cadastro de Usuário')


@app.route('/index')
def index():
    if 'usuario' not in session or session['usuario'] == None:
        return redirect(url_for('login'))
    SQL_GERAL = "SELECT id_user, usuario, nivel_acesso from users order by id_user ASC"
    resSelect = f.consulta_bd(SQL_GERAL)
    idUsuario, usuario, permissao = separaUser(resSelect)
    tamanho = len(usuario)
    return render_template('Lista.html', titulo='Portal de Gerenciamento de Usuários',
                           idUsuario=idUsuario, usuario=usuario,
                           permissao=permissao, tamanho=tamanho)


@app.route('/novo')
def novo():
    if 'usuario' not in session or session['usuario'] == None:
        return redirect(url_for('login'))
    return render_template('Novo.html', titulo='Formulário de Cadastro de Usuários')

@app.route('/editar/<string:id>', methods=['GET','POST'])
def editar(id):
    SQL_EDITAR = "SELECT id_user, usuario, nivel_acesso from users where id_user = '{0}'".format(id)
    resultado = f.consulta_bd(SQL_EDITAR)
    idUsuario, usuario, permissao = separaUser(resultado)
    if 'usuario' not in session or session['usuario'] == None:
        return redirect(url_for('login'))
    if request.method == "GET":
        return render_template('Editar.html', titulo='Formulário para Alteração de Permissão de Usuário',
                               idUsuario=idUsuario,
                               usuario=usuario,
                               permissao=permissao)
    else:
        
        upUsuario = request.form['usuario']
        upPermissao = request.form['permissao']
        SQL_EDITA = "UPDATE users SET usuario = '{0}', nivel_acesso = '{1}' where id_user = '{2}'".format(upUsuario, upPermissao, idUsuario[0])
        f.inserir_bd(SQL_EDITA)
        #flash('Alteração realizada com sucesso!')
        return redirect(url_for('index'))

@app.route('/deletar/<string:id>')
def deletar(id):
    SQL_DELETA = "DELETE from users where id_user = '{0}'".format(id)
    f.inserir_bd(SQL_DELETA)
    #flash('Endpoint removido com sucesso!')
    return redirect(url_for('index'))


@app.route('/alterarsenha/<string:id>', methods=['GET','POST'])
def senha(id):
    SQL_SENHA = "SELECT usuario from users where id_user = '{0}'".format(id)
    resultado = f.consulta_bd(SQL_SENHA)
    usuario = resultado[0]
    if 'usuario' not in session or session['usuario'] == None:
        return redirect(url_for('login'))
    if request.method == "GET":
        return render_template('Alterar.html', titulo='Formulário para Alteração de Senha de Usuário',
                               
                               usuario=usuario,
                               idUsuario=id,
                               )
    else:
        
        senha = request.form['senha']
        
        SQL_EDITA = "UPDATE users SET senha = '{0}' where id_user = '{1}'".format(senha, id)
        f.inserir_bd(SQL_EDITA)
        #flash('Alteração realizada com sucesso!')
        return redirect(url_for('index'))


@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    senha = request.form['senha']
    permissao = request.form['permissao']
    ultimoid = f.consulta_bd("select id_user from users order by id_user DESC")
    resultado = ultimoID(ultimoid)
    SQL_PORTA = "SELECT * from users where usuario = '{0}'".format(nome)
    resSelect = f.consulta_bd(SQL_PORTA)
    if resSelect == []:
        SQL_CRIA = "INSERT into users (id_user, usuario, senha, nivel_acesso) values ('{3}','{0}', '{1}', {2})".format(nome, senha, permissao, int(resultado[0])+1)
        f.inserir_bd(SQL_CRIA)
        return redirect(url_for('index'))
    else:
        flash('o usuário ' + nome + ' já se encontra cadastrada no sistema. Por favor, tente outra.')
        return render_template('Novo.html')

app.run(debug=True, port=5010)            