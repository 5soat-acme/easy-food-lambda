# Easy Food Infra Lmabda

## Arquivos Terraform e Lambda
Na pasta **terraform** há os arquivos do Terraform para gerenciar a infraestrutura de Lambda e Cognito do projeto **[Easy Food](https://github.com/5soat-acme/easy-food)**. As lambdas estão na pasta **lambdas**.

Os arquivos Terraform contidos nesse repositório cria a seguinte infraestrutura na AWS:
- Cognito para gerenciar usuários.
- Lambda para criação de usuário no Cognito.
- Lambda para autenticação de usuário no Cognito.
- API Gateway para expor enpoint para a chamada das lambdas.

**Obs.:** Necessário informar no arquivo **terraform/variables.tf** as informações referentes a conta da AWS Academy

## Workflow - Github Action
O repositório ainda conta com um workflow para criar a infraestrutura na AWS quando houver **push** na branch **main**.

Para o correto funcionamento do workflow é necessário configurar as seguintes secrets no repositório, de acordo com a conta da AWS Academy:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_SESSION_TOKEN

## Criação de Usuário
Para criar um usuário, basta pegar o endpoint gerado pela API Gateway e fazer uma requisição POST na seguinte URL:
```
https://XXXXXX.execute-api.us-east-1.amazonaws.com/create-user
```
Exemplo de Json para criação de usuário:
```
{
  "name": "Nome do usuário",
  "cpf": "11111111111",
  "password": "Senha123_",
  "email": "exmpleo@teste.com"
}
```

## Autenticação de Usuário (Geração do Token)
Para autenticar um usuário, basta pegar o endpoint gerado pela API Gateway e fazer uma requisição POST na seguinte URL:
```
https://XXXXXX.execute-api.us-east-1.amazonaws.com/auth
```
Exemplo de Json para autenticação de usuário:
```
{
  "cpf": "11111111111",
  "password": "Senha123_"
}
```
