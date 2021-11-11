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

- Executar coverage

```shell
 coverage run --source=dock/ -m pytest
 coverage report -m
```



## API Reference
[`insomnia.json`](https://github.com/mpluiz/dock-app/blob/master/insomnia.json)

`BasePath: '/api/v1'`

---

#### Add a new account

```http
  POST /accounts
```

---

#### Find account

```http
  GET accounts/{accountId}/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `accountId`| `String` | **Required**. |

---

#### Make a deposit

```http
  POST /accounts/{accountId}/deposit/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `accountId`| `String` | **Required**. |

---

#### Make withdrawal if have daily limit

```http
  POST /accounts/{accountId}/withdraw/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `accountId`| `String` | **Required**. |

---

#### Deactivate account

```http
  PATCH /accounts/{accountId}/deactivate/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `accountId`| `String` | **Required**. |

---

#### Activate Account

```http
  PATCH /accounts/{accountId}/activate/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `accountId`| `String` | **Required**. |

---

#### Find account transactions

```http
  PATCH /accounts/{accountId}/transactions?start_date=2021-07-24&end_date=2021-07-25
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `accountId`| `String` | **Required**. |
| `start_date`| `Query String` | **Required**. |
| `end_date`| `Query String` | **Required**. |

## License

[MIT](https://choosealicense.com/licenses/mit/)

