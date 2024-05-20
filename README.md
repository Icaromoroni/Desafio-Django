<h1 align="center">
<img src="./images/image.png">
<p>Order Manager</p>
</h1>

## Sobre 💬
**Desafio Django:** recebi uma tarefa de criar uma API RESTful que gerencia usuários, pedidos e itens. O app do projeto foi nomeado como **Order Manager** pois retrata sua tarefa de gerenciar pedidos de itens por usuário.

O app gerencia a criação, autenticação, lista, atualização e visualização dos detalhes dos dados de usuários e suas permissoes no sistema, de maneira semelhante realiza a gestão de itens e pedidos.

## Ferramentas 🔧
- [Django](https://www.djangoproject.com/)
- [Django REST framwork](https://www.django-rest-framework.org/)
- [PostrgreSQL](https://www.postgresql.org/)
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/)

## Configurar o projeto 💻
### Requisitos
- Python 3.6 +
- virtualenv
- PostgreSQL
### Clona o projeto
```bash
$ git clone git@github.com:Icaromoroni/Desafio-Django.git
```
### Entra na pasta "Desafio-Django"
```bash
$ cd Desafio-Django
```
### Cria o ambiente virtual
```bash
# Linux
$ python3 -m venv venv

# Windows
$ python -m venv venv
```

### Ativa o ambiente virtual

```bash
# Linux
$ source venv/bin/activate

# Windows
$ venv/Scripts/activate
```
### Instala as dependências
```bash
$ pip freeze > requirements.txt
```
### Cria o arquivo ".env"
```code
DB_NAME = nome_do_banco_de_dados
DB_USER = usuario do DB
DB_PASSWORD = senha
DB_HOST = localhost
DB_PORT = 5432
```
## Executar o projeto 🙌
### Entra na pasta "management"
```bash
$ cd management
```
### Executa as migrações do banco de dados
```bash
$ python manage.py makemigrations
$ python manage.py migrate
```
### Cria um super usuário
```bash
$ python manage.py createsuperuser
```
### Execulta o servidor
```bash
$ python manage.py runserver
```
### Acessa a rota da documentação
<http://localhost:8000/api/swagger/>

<p>Realiza o login com o nome do usuário e senha que no item "criar um super usuário", após fazer o login é so seguir as descrições nos endpoints</p>

### Exemplo em vídeo abaixo
![Video de exemplo para ralizar a autenticação do usuário.](https://youtu.be/4qG0Vh6cDF8)

