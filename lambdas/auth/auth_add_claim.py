import uuid

def lambda_handler(event, context):
    
    # Obtenha os atributos do usuário do evento
    user_attributes = event['request']['userAttributes']
    
    # Adicione claims personalizadas ao token JWT
    custom_claims = {
        'session_id': str(uuid.uuid4()),
        'user_cpf': event['userName'],
        'name': user_attributes.get('name', ''),
        'email': user_attributes.get('email', ''),
        'user_type': 'registred'
    }
    
    # Adicione as claims personalizadas ao evento
    event['response'] = {
        'claimsOverrideDetails': {
            'claimsToAddOrOverride': custom_claims
        }
    }
    
    return event