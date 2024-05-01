import os
import boto3
import json

def lambda_handler(event, context):

    request_body = event["body"]
    request_data = json.loads(request_body)

    # Dados de autenticação no Cognito
    client_id = os.environ["COGNITO_CLIENT_ID"]
    cpf = remover_ponto_traco(request_data["cpf"])
    password = request_data["password"]
    
    # Configuração do cliente Cognito
    client = boto3.client('cognito-idp')
    
    # Autenticação no Cognito
    try:
        auth_response = client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': cpf,
                'PASSWORD': password
            },
            ClientId=client_id
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps(auth_response["AuthenticationResult"])
        }
    
    except client.exceptions.NotAuthorizedException as e:
        return {
            'statusCode': 401,
            'body': json.dumps({'error': str(e)})
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