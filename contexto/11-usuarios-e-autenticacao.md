# Usuários e autenticação

Autenticação confirma identidade; autorização determina acesso. Django oferece autenticação, login/logout e `login_required` para proteger views e redirecionar usuários sem sessão à rota de login configurada.

Relacionar registros ao usuário com `ForeignKey` separa dados por conta. Listar, editar e remover filtrando pelo usuário autenticado impede acesso aos dados de outras contas. A view pode associar o usuário ao objeto sem expor esse campo no formulário.

Django armazena senhas com hash. `UserCreationForm` serve de base para cadastro; os slides mostram adicionar e-mail/nome e validar antes de salvar.
