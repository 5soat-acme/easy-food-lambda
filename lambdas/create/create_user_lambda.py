import os
import boto3
import json

def lambda_handler(event, context):

    request_body = event["body"]
    request_data = json.loads(request_body)

    # Dados do usuário a serem inseridos
    user_pool_id = os.environ["COGNITO_USER_POOL_ID"]
    client_id = os.environ["COGNITO_CLIENT_ID"]
    name = request_data['name']
    cpf = remover_ponto_traco(request_data["cpf"])
    password = request_data['password']
    email = request_data['email']

    if not validar_cpf(cpf):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'CPF invalido'})
        }
    
    # Configuração do cliente Cognito
    client = boto3.client('cognito-idp')
    
    # Inserção do usuário no Cognito
    try:
        client.sign_up(
            ClientId=client_id,
            Username=cpf,
            Password=password,
            UserAttributes=[
                {'Name': 'name', 'Value': name},
                {'Name': 'email', 'Value': email}
            ]
        )

        client.admin_confirm_sign_up(
            UserPoolId=user_pool_id,
            Username=cpf
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Usuario inserido com sucesso!'})
        }
    except client.exceptions.UsernameExistsException as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'O usuario ja existe'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def remover_ponto_traco(texto):
    texto_sem_ponto = texto.replace('.', '')
    texto_sem_ponto_traco = texto_sem_ponto.replace('-', '')
    return texto_sem_ponto_traco

def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))

    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10) % 11
    if digito1 == 10:
        digito1 = 0

    if digito1 != int(cpf[9]):
        return False

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10) % 11
    if digito2 == 10:
        digito2 = 0

    if digito2 != int(cpf[10]):
        return False

    return True