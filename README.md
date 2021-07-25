# Dock APP

API REST para sistema de gestão de contas

## Requisitos 
- Docker
- Docker Compose
- Python 3.x para desenvolvimento e testes


### Clone o repositório

- Em seu terminal, navegue até a pasta de preferências e execute o comando, isso fará o download de todos os arquivos em sua máquina.

```shell
git clone https://github.com/mpluiz/dock-app.git
```

### Configuração 

- Executar docker-compose para iniciar a aplicação

```shell
docker-compose build && docker-compose up -d
```

### Configuração para desenvolvimento e testes

- Criar virtualenv

```shell
python -m venv .venv
```

- Ativar virtualenv

```shell
source .venv/bin/activate
```

- Instalar dependências

```shell
pip install -r requirements.txt
```

- Executar testes

```shell
pytest
```

### API

```php
InsomniaFile: [insomnia.json](https://github.com/mpluiz/dock-app/blob/master/docs/insomnia.json)
BasePath: `/api/v1`
```

```php
Method: POST
Endpoint: `/accounts`

Add a new account
```

```php
Method: GET
Endpoint: `accounts/{accountId}/`

Find account
```

```php
Method: POST
Endpoint: `/accounts/{accountId}/deposit/`

Make a deposit
```

```php
Method: POST
Endpoint: `/accounts/{accountId}/withdraw/`

Make a withdrawal
```

```php
Method: PATCH
Endpoint: `/accounts/{accountId}/deactivate/`

Deactivate account
```

```php
Method: PATCH
Endpoint: `/accounts/{accountId}/activate/`

Activate Account
```

```php
Method: GET
Endpoint: `/accounts/{accountId}/transactions/`
QueryParams: `?start_date=2021-07-24&end_date=2021-07-25`

Find account transaction
```
