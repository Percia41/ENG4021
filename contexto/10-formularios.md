# Formulários

Formulários enviam dados ao servidor. GET coloca parâmetros no endereço e serve a buscas/filtros; POST envia dados no corpo e é usado nos exemplos de alteração. Elementos HTML: `form`, `input`, `textarea`, `select`, `label` e botão. Campos aceitam obrigatoriedade, limites e valores iniciais.

Django: `forms.Form` define formulário independente; `forms.ModelForm` deriva campos de um modelo. Validar os dados antes de salvar. O template exibe o formulário; POST deve incluir `{% csrf_token %}`. A view pode salvar e redirecionar.

CRUD = criar, ler, atualizar e remover. Os slides mostram inserir, listar, editar e remover uma referência, com confirmação da remoção. O PDF de Formulários repete conteúdo de Python, HTML, CSS, Django e modelos; essa repetição foi removida e os conceitos estão nos respectivos contextos.
