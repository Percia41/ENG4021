# ENG4021

## Moda com Pequenos Defeitos, Preço Justo

Projeto da disciplina **ENG4021 — Projeto de Software**.

A proposta é criar uma plataforma para divulgar peças de roupa com pequenos
defeitos de fabricação, explicando o defeito e o desconto aplicado de forma
transparente.

## 1. Organização geral do projeto

Este repositório reúne os materiais desenvolvidos ao longo das sprints e o
aplicativo web principal. A organização geral é:

```text
ENG4021/
├── README.md                 # Documentação geral do projeto
├── Sprint 0/                 # Materiais e exercícios da Sprint 0
├── Sprint 1/                 # Materiais e exercícios da Sprint 1
├── Sprint 2/                 # Materiais e exercícios da Sprint 2
├── ...                       # Próximas sprints
└── fio-fora/                 # Repositório específico do aplicativo Django
```

### Guia de organização

- Todo arquivo, exercício, código ou documentação referente a uma sprint deve
    ficar dentro da pasta correspondente: `Sprint 0`, `Sprint 1`, `Sprint 2` e
    assim por diante.
- A pasta de uma sprint deve reunir apenas os materiais daquela etapa, para
    que seja possível acompanhar a evolução do projeto sem misturar versões ou
    atividades diferentes.
- A pasta `fio-fora` contém o projeto codado do aplicativo e sua própria
    estrutura Django. A explicação técnica dessa parte está documentada a partir
    da seção seguinte.
- Este `README.md` apresenta primeiro a organização geral do repositório e,
    depois, a instalação, a arquitetura e o estado atual do aplicativo.

## 2. Repositório específico do aplicativo: `fio-fora`

Esta é a parte do projeto que já foi implementada em código. O aplicativo é uma
plataforma Django para exibir produtos com pequenos defeitos de fabricação,
informar o defeito e apresentar um preço reduzido de forma transparente. Os
arquivos do sistema ficam dentro de `fio-fora/`; as pastas de sprint não
fazem parte da estrutura interna do aplicativo.

### 2.1 Instalação

### Instalar o Python

Se necessário, antes de instalar o projeto, instale o Python no seu computador. Baixe sempre
o instalador no site oficial: <https://www.python.org/downloads/>.

#### Windows

1. Acesse o site do Python e baixe a versão para Windows.
2. Execute o instalador baixado.
3. Na primeira tela, marque **Add python.exe to PATH**.
4. Clique em **Install Now** e aguarde a conclusão.
5. Abra o PowerShell e confirme a instalação:

```powershell
python --version
```

Se aparecer a versão do Python, a instalação está pronta.

#### macOS

1. Acesse o site do Python e baixe o instalador para macOS (`.pkg`).
2. Abra o arquivo baixado e siga as etapas do instalador.
3. Ao terminar, abra o Terminal e confirme a instalação:

```bash
python3 --version
```

Se aparecer a versão do Python, a instalação está pronta.

#### Fedora Linux

1. Abra o Terminal.
2. Instale o Python e o `pip` usando o gerenciador de pacotes do Fedora:

```bash
sudo dnf install python3 python3-pip
```

3. Confirme a instalação:

```bash
python3 --version
```

Se aparecer a versão do Python, a instalação está pronta.

#### Ubuntu, Pop!_OS e Debian

1. Abra o Terminal.
2. Instale o Python, o `pip` e o módulo `venv`:

```bash
sudo apt install python3 python3-pip python3-venv
```

3. Confirme a instalação:

```bash
python3 --version
```

Se aparecer a versão do Python, a instalação está pronta.

### Inicializar e rodar o projeto

Se você está na pasta `ENG4021`, entre na pasta do projeto:

```bash
cd fio-fora
```

Depois, use os comandos do seu sistema abaixo.

#### Codespace, Linux e macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m django --version
python manage.py migrate
python manage.py check
python manage.py runserver
```

#### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m django --version
python manage.py migrate
python manage.py check
python manage.py runserver
```

O comando `python manage.py migrate` cria as tabelas internas que o Django
precisa para funcionar, como as tabelas de usuários, sessões e administração.

Depois, acesse <http://127.0.0.1:8000/> no navegador. Essa página é o login;
a vitrine fica em <http://127.0.0.1:8000/vitrine/>. Para parar o servidor,
use `Ctrl+C`.

Para entrar no Django Admin (`/admin/`), crie antes um usuário administrador:

```bash
python manage.py createsuperuser
```

### Rodar de novo depois da instalação

A instalação só precisa ser feita uma vez. Nas próximas vezes, basta ativar o
ambiente virtual e iniciar o servidor.

#### Codespace, Linux e macOS

```bash
cd fio-fora
source .venv/bin/activate
python manage.py migrate
python manage.py runserver
```

#### Windows (PowerShell)

```powershell
cd fio-fora
.venv\Scripts\Activate.ps1
python manage.py migrate
python manage.py runserver
```

Depois de puxar alterações com `git pull`, rode `python manage.py migrate`
antes do `runserver`, pois outra pessoa pode ter alterado os models.

### Problemas comuns

- **`Command 'python' not found` depois de ativar o `.venv`:** o ambiente
    virtual foi criado em outra pasta (por exemplo, na antiga `moda-defeitos`).
    O `.venv` guarda o caminho onde foi criado e não funciona se a pasta for
    movida ou renomeada. Apague e crie de novo dentro de `fio-fora`:

    ```bash
    deactivate
    rm -rf .venv
    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt
    ```

- **`Error: That port is already in use`:** já existe um servidor rodando em
    outro terminal. Pare-o com `Ctrl+C` ou use outra porta:
    `python manage.py runserver 8001`.

## 2.2 Tecnologias utilizadas

- Python
- Django
- HTML e CSS

## 2.3 Padrões de projeto

O projeto segue a organização natural do Django, baseada no padrão
**Model-Template-View (MTV)**. Em muitos materiais em português, esse mesmo
jeito de organizar o Django aparece como **MVT**. A ideia é a mesma: separar os
dados, a aparência da página e o código que responde às ações do usuário.

Esse padrão é realmente usado no Django. A documentação oficial apresenta
separadamente o model, a view, o template, as URLs e os formulários, e mostra
como eles trabalham juntos. Veja o exemplo oficial em
<https://docs.djangoproject.com/en/5.2/intro/overview/>.

```text
URL → View → Model/Form → Template → HTML + CSS
```

Na vitrine, a URL `/vitrine/` chama a view `home`, que busca os `Product` e
envia a lista para o template. No cadastro de peça, a URL chama outra view, que
usa o `ProductForm`, salva a peça e volta para "Minhas peças".

### Estrutura interna de `fio-fora`

O projeto segue o padrão do tutorial oficial do Django: a pasta `config/` guarda
só a configuração e cada **app** cuida de uma área do site, com seus próprios
models, views, URLs, templates, CSS e testes. O que é usado por todas as páginas
(layout, cabeçalho, CSS geral) fica em `templates/` e `static/` na raiz.

```text
fio-fora/
├── manage.py                 # Comandos do Django
├── requirements.txt          # Dependências do projeto
├── config/                   # Configuração geral (settings.py, urls.py, wsgi.py, asgi.py)
│
├── templates/                # HTML compartilhado por todas as páginas
│   ├── base.html             # Estrutura da página: <head>, cabeçalho e mensagens
│   └── components/           # Pedaços reutilizáveis (incluídos com {% include %})
│       ├── header.html       # Cabeçalho único, com links conforme o tipo de conta
│       ├── messages.html     # Mensagens de sucesso e erro
│       ├── form_fields.html  # Todos os campos de um formulário
│       ├── field.html        # Um campo de formulário
│       ├── pagination.html   # Paginação
│       └── logo.html
├── static/                   # CSS, fontes e imagens compartilhados
│   ├── css/                  # site.css importa variables, reset, logo, controls e layout
│   ├── icons/ e fonts/       # Bootstrap Icons
│   └── images/               # Logo
│
├── accounts/                 # Contas: login, cadastro, perfil, senha e lista de usuários
│   ├── models.py             # UserProfile (tipo de conta, loja, documento...)
│   ├── decorators.py         # Quem pode o quê: buyer_required, seller_required
│   ├── context_processors.py # is_buyer e is_seller disponíveis em todo template
│   └── backends.py           # Login usando o e-mail
├── products/                 # Catálogo e área do vendedor
│   ├── models.py             # Product, Defeito, Category, ProductImage e a fórmula de severidade
│   ├── forms.py              # ProductForm (cadastrar/editar) e simulador de desconto
│   └── management/commands/  # popular_banco (dados de exemplo)
├── cart/                     # Carrinho
│   └── services.py           # Regras de estoque e total, usadas também no checkout
├── orders/                   # Checkout e pedidos
│   └── services.py           # Finalização da compra
└── favorites/                # Favoritos
```

Todo app segue o mesmo formato:

```text
<app>/
├── models.py, views.py, urls.py, forms.py, admin.py, tests.py
├── migrations/
├── templates/<app>/          # HTML do app (o nome do app se repete para evitar conflito)
│   └── includes/             # Pedaços do app reaproveitados em outras páginas
└── static/<app>/css/         # CSS do app
```

### O que cada parte faz usando o produto como exemplo

#### 1. `config/settings.py`: configurações do projeto

Esse arquivo diz ao Django quais recursos o projeto usa: apps instalados,
templates, arquivos estáticos e banco de dados. Não é o lugar para escrever a
lógica do produto.

```python
INSTALLED_APPS = [
    # apps do Django...
    'accounts',
    'products',
    'cart',
    'orders',
    'favorites',
]
```

As pastas `templates/` e `static/` da raiz são registradas em `TEMPLATES['DIRS']`
e `STATICFILES_DIRS`.

#### 2. `config/urls.py` e `<app>/urls.py`: caminhos das páginas

`config/urls.py` é a entrada principal e só encaminha para as URLs de cada app.
Em `products/urls.py`, por exemplo, `/vitrine/` chama a vitrine e
`/produtos/novo/` chama o cadastro de peça. O caminho `/` fica em
`accounts/urls.py` e abre a página de login.

```python
path('vitrine/', views.home, name='home'),
path('produtos/novo/', views.product_create, name='product_create'),
```

#### 3. `products/models.py`: os dados do produto

O model é uma classe Python que representa um tipo de dado salvo no banco.
`Product` representa uma peça da vitrine e `Defeito` guarda os três critérios do
defeito (tipo, localização e extensão), ligado 1-para-1 à peça:

```python
class Product(models.Model):
    name = models.CharField("nome", max_length=120)
    description = models.TextField("descrição")
    price = models.DecimalField("preço final", max_digits=10, decimal_places=2)
    is_active = models.BooleanField("produto ativo", default=True)
```

A severidade, a faixa (Leve, Moderada, Alta) e o desconto sugerido são
calculados pelo model, a partir do `Defeito`. Existe uma única fórmula, em
`severidade()`.

#### 4. `products/forms.py`: formulário da peça

O `ProductForm` é usado tanto para cadastrar quanto para editar uma peça. O
vendedor informa o preço original e os critérios do defeito; o preço final é
calculado pelo model, nunca enviado pelo navegador.

```python
class ProductForm(DefectFieldsMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'category', 'description', 'original_price', ...]
```

#### 5. `products/views.py`: o que acontece em cada página

A view recebe a requisição e devolve uma resposta. A vitrine busca as peças
ativas e envia para o template:

```python
products = Product.objects.filter(is_active=True)
return render(request, 'products/home.html', {'products': products})
```

As páginas restritas usam os decorators de `accounts/decorators.py`:

```python
@seller_required
def product_create(request):
    ...
```

#### 6. Templates: o HTML que a pessoa vê

`templates/base.html` guarda a estrutura comum: o `<head>`, o cabeçalho e as
mensagens. Cada página herda essa estrutura e preenche o bloco `content`:

```html
{% extends 'base.html' %}

{% block content %}
    ...
{% endblock %}
```

Os apps que têm CSS próprio têm um `base.html` que só acrescenta esse CSS (por
exemplo, `products/base.html`). Pedaços repetidos ficam em arquivos próprios e
são incluídos com `{% include %}`:

```html
{% include 'components/form_fields.html' %}
{% include 'products/includes/card_info.html' %}
{% include 'cart/includes/add_button.html' %}
```

#### 7. CSS: a aparência da página

O CSS geral fica em `static/css/` e é carregado em todas as páginas por
`site.css`. Cada app tem o seu, em `<app>/static/<app>/css/`, por exemplo
`products/static/products/css/products.css`. No template:

```html
{% load static %}
<link rel="stylesheet" href="{% static 'products/css/products.css' %}">
```

Os campos dos formulários são estilizados pelo CSS (`.form-field input`), então
não é preciso colocar classes nos widgets em Python.

#### 8. `admin.py`: gerenciamento pelo Admin

Cada app registra os próprios models em `/admin/`:

```python
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_active']
```

#### 9. `tests.py`: verificar se o código funciona

Cada app tem seus testes em `tests.py`. Eles simulam ações sem abrir o
navegador. Para rodar todos:

```bash
python manage.py test
```

#### 10. `migrations/`: registrar mudanças no banco

Quando alteramos um model, o Django precisa atualizar a estrutura do banco. Não
editamos os arquivos dessa pasta manualmente. Usamos:

```bash
python manage.py makemigrations
python manage.py migrate
```

`makemigrations` registra a mudança e `migrate` aplica a mudança no banco.

## 2.4 Estado atual das funcionalidades

- login na página inicial (`/`), cadastro de comprador, vendedor e marca em
    `/cadastro/`, recuperação de senha em `/recuperar-senha/` e perfil em `/conta/`;
- vitrine em `/vitrine/`, com filtro por faixa de severidade;
- página da peça em `/produtos/<id>/`;
- área do vendedor: `/minhas-pecas/`, cadastro em `/produtos/novo/`, edição em
    `/produtos/<id>/editar/` e remoção em `/produtos/<id>/remover/`;
- simulador de desconto em `/simulador/`;
- carrinho em `/carrinho/`, favoritos em `/favoritos/`, checkout em `/checkout/`
    e pedidos em `/pedidos/`;
- lista de usuários para a equipe em `/usuarios/`;
- gerenciamento pelo Django Admin em `/admin/`;
- dados de exemplo com `python manage.py popular_banco`.

Depois de atualizar o código, execute `python manage.py migrate` dentro de
`fio-fora`. Se o seu `db.sqlite3` for de antes da divisão em apps, apague-o e
rode `python manage.py migrate` e `python manage.py popular_banco` de novo.
