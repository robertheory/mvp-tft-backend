# Total Fitness Tracker (TFT)

## Descrição

O Total Fitness Tracker (TFT) é um MVP desenvolvido para a avaliação da pós-graduação em Engenharia de Software da PUC-Rio - Pontifícia Universidade Católica do Rio de Janeiro.

Este sistema tem como objetivo auxiliar os usuários no monitoramento de sua dieta e evolução corporal, permitindo o registro de refeições, controle de calorias e acompanhamento histórico de peso e nível de atividade física.

Descrição completa disponível em [docs/specs.md](docs/specs.md).

## Instalação e Execução da API

### Pré-requisitos

- [Python](https://www.python.org/downloads/) (versão 3.8 ou superior)
- Virtualenv (opcional, mas recomendado)

### Passos para Instalação

Clone o repositório:

```bash
git clone https://github.com/robertheory/backend-tft.git
cd tft-mvp
```

Crie e ative um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv env
source env/bin/activate # Linux/macOS
env\Scripts\activate # Windows
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Executando a API

Para iniciar a API, execute o seguinte comando no diretório raiz do projeto:

```bash
flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento, utilize o modo reload para que as mudanças no código sejam refletidas automaticamente:

```bash
flask run --host 0.0.0.0 --port 5000 --reload
```

Acesse `http://localhost:5000/#/` no navegador para visualizar a documentação da API e testar os endpoints.
