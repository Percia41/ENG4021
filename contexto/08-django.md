# Django — estrutura de aplicativo web

Fluxo básico: URL → view → modelo/banco de dados, quando preciso → template HTML → resposta ao navegador.

- `urls.py`: associa caminhos a views.
- `views.py`: recebe requisições, prepara dados e renderiza templates.
- Templates: exibem dados e usam condicionais/laços Django.
- `models.py`: descreve dados persistidos; migrations aplicam mudanças ao banco.
- `forms.py`: define e valida formulários.
- `admin.py`: configura interface administrativa.
- `static`: CSS e arquivos estáticos.

Os slides mostram criar projeto/app, registrar o app em `INSTALLED_APPS`, renderizar páginas e passar variáveis/listas/dicionários ao template. Também demonstram parâmetros na URL. Conferir comandos e versões no ambiente atual.
