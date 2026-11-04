# Modelagem de dados

Organiza dados em tabelas, campos e relações. Modelos Django descrevem dados persistidos; campos comuns incluem texto, e-mail, URL, booleano, inteiro, decimal, data/hora e chave estrangeira, com opções, valores padrão e validações.

`ForeignKey` relaciona modelos. Exemplos dos slides: `Prova`, `Questão` e `Referência`, com ordenação, `__str__` e configuração do admin. Após alterar modelos, executar `makemigrations` e `migrate`. Admin permite listar, ordenar, filtrar e editar registros. A ORM busca, filtra, ordena e recupera objetos. Exemplos SQL (`CREATE TABLE`, `INSERT`, `SELECT`) mostram a relação com tabelas de banco relacional.
