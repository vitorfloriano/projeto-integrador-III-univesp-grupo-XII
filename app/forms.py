from django import forms
from django.core.validators import RegexValidator

class ContatoForm(forms.Form):
    """
    Formulário para a página de contato
    """
    nome = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'id': 'nome', 'placeholder': 'Nome', 'required': True, 'aria-required': 'true'}),
        label='Nome'
    )
    telefone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'id': 'telefone', 'placeholder': 'Telefone', 'required': True, 'aria-required': 'true'}),
        validators=[
            RegexValidator(
                regex=r'^\(\d{2}\)\s?\d{4,5}-\d{4}$|^\d{10,11}$',
                message='Formato de telefone inválido. Use (XX) XXXXX-XXXX ou XXXXXXXXXXX'
            )
        ],
        label='Telefone'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'id': 'email', 'placeholder': 'E-mail', 'required': True, 'aria-required': 'true'}),
        label='E-mail'
    )
    endereco = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'id': 'endereco', 'placeholder': 'Endereço', 'required': True, 'aria-required': 'true'}),
        label='Endereço'
    )
    estado = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'id': 'estado', 'placeholder': 'Estado', 'required': True, 'aria-required': 'true'}),
        label='Estado'
    )
    cidade = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'id': 'cidade', 'placeholder': 'Cidade', 'required': True, 'aria-required': 'true'}),
        label='Cidade'
    )
    mensagem = forms.CharField(
        widget=forms.Textarea(attrs={'id': 'mensagem', 'placeholder': 'Mensagem', 'rows': '5', 'required': True, 'aria-required': 'true'}),
        label='Mensagem'
    )

class EmpregoForm(forms.Form):
    """
    Formulário para a página 'Trabalhe Conosco'
    """
    nome_c = forms.CharField(
        label='Nome Completo',
        max_length=150,
        widget=forms.TextInput(attrs={'id': 'nome_c', 'class': 'inputUser', 'required': True, 'aria-required': 'true'})
    )
    data_nasc = forms.DateField(
        label='Data de Nascimento',
        widget=forms.DateInput(attrs={'id': 'data_nasc', 'type': 'date', 'class': 'inputUser', 'required': True, 'aria-required': 'true'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'id': 'email', 'class': 'inputUser', 'required': True, 'aria-required': 'true'})
    )
    telefone = forms.CharField(
        label='Telefone',
        max_length=15,
        widget=forms.TextInput(attrs={'id': 'telefone', 'class': 'inputUser', 'required': True, 'aria-required': 'true'}),
        validators=[
            RegexValidator(
                regex=r'^\(\d{2}\)\s?\d{4,5}-\d{4}$|^\d{10,11}$',
                message='Formato de telefone inválido. Use (XX) XXXXX-XXXX ou XXXXXXXXXXX'
            )
        ]
    )
    endereco = forms.CharField(
        label='Endereço',
        max_length=200,
        widget=forms.TextInput(attrs={'id': 'endereco', 'class': 'inputUser', 'required': True, 'aria-required': 'true'})
    )
    objetivo = forms.CharField(
        label='Objetivo',
        required=False,
        widget=forms.Textarea(attrs={'id': 'objetivo', 'cols': '90', 'rows': '5', 'class': 'inputUser'})
    )
    formacao = forms.CharField(
        label='Formação Acadêmica/Cursos',
        required=False,
        widget=forms.Textarea(attrs={'id': 'formacao', 'cols': '90', 'rows': '5', 'class': 'inputUser'})
    )
    experiencia = forms.CharField(
        label='Experiência profissional',
        required=False,
        widget=forms.Textarea(attrs={'id': 'experiencia', 'cols': '90', 'rows': '5', 'class': 'inputUser'})
    )
