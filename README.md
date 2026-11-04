# ENG4021 — FioFora

Projeto da disciplina **ENG4021 — Projeto de Software**.

**FioFora** é uma plataforma web de moda circular: marcas e vendedores anunciam
peças com pequenos defeitos de fabricação, o defeito é explicado com
transparência e o desconto é calculado a partir da gravidade dele.

> **[PRINT]** Vitrine do FioFora com alguns cards de peças e o filtro de severidade visível.

## Sumário

- [Organização do repositório](#organização-do-repositório)
- [Rodar o projeto](#rodar-o-projeto)
- [Documentação do aplicativo](#documentação-do-aplicativo)

## Organização do repositório

```text
ENG4021/
├── README.md        # Este arquivo
├── AGENTS.md        # Padrões do projeto para agentes de IA
├── fio-fora/        # Aplicativo Django (todo o código fica aqui)
└── Sprint N/        # Entregas de cada sprint que não são código
```

- **`fio-fora/`** guarda todo o código do aplicativo.
- **Pastas `Sprint N/`** guardam só o que **não é código** de cada sprint:
    pesquisas, entrevistas, PDFs, planilhas, protótipos e apresentações.
    Código de qualquer sprint vai para `fio-fora/`.

## Rodar o projeto

No Codespace ou no Linux, a partir da pasta `ENG4021`:

```bash
cd fio-fora && python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt && python manage.py migrate && python manage.py popular_banco && python manage.py runserver
```

Abra <http://127.0.0.1:8000/>. Para Windows, macOS e outros detalhes, veja a
[documentação do aplicativo](fio-fora/README.md#instalação).

## Documentação do aplicativo

**[fio-fora/README.md](fio-fora/README.md)** é a documentação principal. Ela
explica a organização do Django, os conceitos usados, o banco de dados e o que
cada app faz, com links para a documentação de cada um.
