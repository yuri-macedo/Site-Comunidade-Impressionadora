from flask import render_template, redirect, url_for, flash, request, abort
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil,FormCriarPost
from comunidadeimpressionadora.models import Usuario,Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image
from datetime import datetime,timezone
import pytz

def converter_hora(utc_tempo):
    tz = pytz.timezone('America/Sao_Paulo')
    return pytz.utc.localize(utc_tempo, is_dst=None).astimezone(tz)

@app.route("/")
def home():
    lista_posts=Post.query.order_by(Post.id.desc())
    return render_template("home.html",lista_posts=lista_posts,converter_hora=converter_hora)

@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route("/usuarios")
@login_required
def usuarios():
    lista_usuarios=Usuario.query.all()
    return render_template("usuarios.html",lista_usuarios=lista_usuarios)

@app.route("/login",methods=["GET","POST"])
def login():
    form_login=FormLogin()
    form_criar_conta=FormCriarConta()

    if form_login.validate_on_submit() and "botao_login" in request.form:
        usuario=Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha,form_login.senha.data):
            login_user(usuario,remember=form_login.lembrar_login.data)
            flash(f"Login feito com sucesso no e-mail: {form_login.email.data}","alert-success")
            par_next=request.args.get("next")
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for("home"))
        else:
            flash("E-mail ou Senha Incorretos",category="alert-danger")
    if form_criar_conta.validate_on_submit() and "botao_criar_conta" in request.form:
        senha_crypt = bcrypt.generate_password_hash(form_criar_conta.senha.data)
        usuario=Usuario(username=form_criar_conta.username.data,email=form_criar_conta.email.data,senha=senha_crypt)
        database.session.add(usuario)
        database.session.commit()
        flash(f"Criada conta para o e-mail: {form_criar_conta.email.data}","alert-success")
        return redirect(url_for("home"))
    return render_template("login.html",form_login=form_login,form_criar_conta=form_criar_conta)

@app.route("/sair")
@login_required
def sair():
    logout_user()
    flash("Logout realizado com sucesso!",category="alert-success")
    return redirect(url_for("home"))

@app.route("/perfil")
@login_required
def perfil():
    lista_cursos = current_user.cursos.split(";")
    return render_template("perfil.html",lista_cursos=lista_cursos)

def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form_editar_perfil = FormEditarPerfil()
    lista_cursos=current_user.cursos.split(";")
    if form_editar_perfil.validate_on_submit():
        current_user.email = form_editar_perfil.email.data
        current_user.username = form_editar_perfil.username.data
        if form_editar_perfil.foto_perfil.data:
            nome_imagem = salvar_imagem(form_editar_perfil.foto_perfil.data)
            current_user.foto_perfil = nome_imagem

        cursos_form=[]
        for campo in form_editar_perfil:
            if "curso_" in campo.name:
                if campo.data:
                    cursos_form.append(campo.label.text)
        current_user.cursos=";".join(cursos_form)


        database.session.commit()
        flash('Perfil atualizado com Sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form_editar_perfil.email.data = current_user.email
        form_editar_perfil.username.data = current_user.username
        for campo in form_editar_perfil:
            if "curso_" in campo.name and campo.label.text in current_user.cursos:
                campo.data=True
    return render_template('editarperfil.html', form_editar_perfil=form_editar_perfil)

@app.route("/post/criar",methods=['GET', 'POST'])
@login_required
def criar_post():
    form_criar_post=FormCriarPost()
    if form_criar_post.validate_on_submit():
        post=Post(titulo=form_criar_post.titulo.data,corpo=form_criar_post.corpo.data,autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash("Post criado com sucesso!","alert-success")
        return redirect(url_for("home"))
    return render_template("criarpost.html",form_criar_post=form_criar_post)

@app.route("/post/<post_id>")
def exibir_post(post_id):
    post=Post.query.get(post_id)
    return render_template("post.html",post=post,converter_hora=converter_hora)

@app.route("/post/<post_id>/editar",methods=["GET","POST"])
def editar_post(post_id):
    post=Post.query.get(post_id)
    form_editar_post=FormCriarPost()
    if form_editar_post.validate_on_submit():
        post.titulo = form_editar_post.titulo.data
        post.corpo = form_editar_post.corpo.data
        database.session.commit()
        return redirect(url_for("home"))
    elif request.method=="GET":
        form_editar_post.titulo.data=post.titulo
        form_editar_post.corpo.data=post.corpo


    return render_template("editarpost.html", post=post, form_editar_post=form_editar_post)

@app.route("/post/<post_id>/excluir",methods=["GET","POST"])
@login_required
def excluir_post(post_id):
    post=Post.query.get(post_id)
    if current_user==post.autor:
        database.session.delete(post)
        database.session.commit()
        flash("Post Excluido com Sucesso","alert-danger")
        return redirect(url_for('home'))
    else:
        abort(403)
