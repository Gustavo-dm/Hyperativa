# Desafio Hyperativa

## Sobre o Desafio
Este projeto implementa uma API para a criação e consulta de números de cartões de crédito completos. A API utiliza autenticação e permite inserção de dados tanto individualmente quanto por arquivos em lote.

## Configuração do Ambiente

### Criar e Ativar o Ambiente Virtual
Para configurar um ambiente virtual Python, siga os passos abaixo no terminal:
```bash
python -m venv venv
source venv/bin/activate  # On Unix or MacOS
venv\Scripts\activate  # On Windows
```

### Executar o projeto Docker Compose
Para rodar o projeto, utilize o comando:
```bash
docker-compose up
```

### Executar o projeto manualmente
Para rodar o projeto manualmente, utilize o comando:
```bash
python manage.py runserver 0.0.0.0:8000
```

### Criação de Superusuário
```bash
python manage.py createsuperuser
```

### Utilização do Swagger

Toda a interação com a API é feita através do Swagger. Após iniciar o servidor, acesse a interface do Swagger em:
```bash
http://localhost:8000/
```
É possível gerar uma token no endpoint
```bash
http://localhost:8000/api/token/
```
utenticação com Token JWT
Gere um token JWT acessando a rota de autenticação em:
```bash

http://localhost:8000/api/token/
```
Envie uma solicitação POST com suas credenciais (e-mail e senha). O formato da solicitação é o seguinte:

```json
{
  "email": "seu-email@example.com",
  "password": "sua-senha"
}
```
Você receberá um access token e um refresh token. Copie o access token.

Na interface do Swagger, clique no botão Authorize no canto superior direito.

Na janela de autenticação, insira o token:

e clique em Authorize.

Agora você está autenticado e pode acessar as rotas protegidas da API.


- **Testes unitários:** 
Para executar os testes 
```bash
python manage.py test
```


###TODO
- Restrições para cartões com o mesmo número
- Logar as requisições de uso da API e seus retornos. - Todos os endpoints
- Utilizar criptografia (end-to-end encryption) para tráfego de informações.
- Pensar em escalabilidade, pode ser uma quantidade muito grande de dados.
