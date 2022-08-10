from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from flask_wtf.file import FileField,FileAllowed
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user

class FormCriarConta(FlaskForm):
    username=StringField("Nome de usuário",validators=[DataRequired()])
    email=StringField("E-mail",validators=[DataRequired(),Email()])
    senha=PasswordField("Senha",validators=[DataRequired(),Length(6,20)])
    confirmacao=PasswordField("Confirmar Senha",validators=[DataRequired(),EqualTo("senha")])
    botao_criar_conta=SubmitField("Criar Conta")
    def validate_email(self,email):
        usuario=Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login.")

class FormLogin(FlaskForm):
    email=StringField("E-mail",validators=[DataRequired(),Email()])
    senha=PasswordField("Senha",validators=[DataRequired(),Length(6,20)])
    lembrar_login=BooleanField("Lembrar Login?")
    botao_login=SubmitField("Login")

class FormEditarPerfil(FlaskForm):
    username=StringField("Nome de usuário",validators=[DataRequired()])
    email=StringField("E-mail",validators=[DataRequired(),Email()])
    foto_perfil = FileField('Alterar imagem', validators=[FileAllowed(['jpg', 'png'])])
    botao_editar_perfil=SubmitField("Confirmar Edição")
    curso_excel=BooleanField("Excel Impressionador")
    curso_vba = BooleanField("VBA Impressionador")
    curso_powerbi = BooleanField("Power Bi Impressionador")
    curso_python = BooleanField("Python Impressionador")
    curso_ppt = BooleanField("PowerPoint Impressionador")
    curso_datascience = BooleanField("Data Science Impressionador")


    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com esse e-mail. Cadastre outro e-mail')


class FormCriarPost(FlaskForm):
    titulo=StringField("Título",validators=[DataRequired(),Length(1,140)])
    corpo=TextAreaField("Escreva Seu Post Aqui",validators=[DataRequired()])
    botao_criar_post=SubmitField("Criar Post")
