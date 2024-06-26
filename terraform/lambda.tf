resource "aws_lambda_function" "create-user-lambda" {
  filename      = "../lambdas/create/create_user_lambda.zip"
  function_name = "create_user_lambda"
  role          = var.labRole
  handler       = "create_user_lambda.lambda_handler"
  runtime       = "python3.8"

  environment {
    variables = {
      COGNITO_USER_POOL_ID = aws_cognito_user_pool.user-pool.id
      COGNITO_CLIENT_ID    = aws_cognito_user_pool_client.user-pool-client.id
    }
  }
}

resource "aws_lambda_function" "auth-add-claim-lambda" {
  filename      = "../lambdas/auth/auth_add_claim.zip"
  function_name = "auth_add_claim"
  role          = var.labRole
  handler       = "auth_add_claim.lambda_handler"
  runtime       = "python3.8"
}

resource "aws_lambda_function" "auth-lambda" {
  filename      = "../lambdas/auth/auth_lambda.zip"
  function_name = "auth_lambda"
  role          = var.labRole
  handler       = "auth_lambda.lambda_handler"
  runtime       = "python3.8"

  environment {
    variables = {
      COGNITO_CLIENT_ID = aws_cognito_user_pool_client.user-pool-client.id
    }
  }
}

# Criando a política de permissão para a função Lambda
resource "aws_lambda_permission" "create-user-lambda_permission-apigw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.create-user-lambda.arn
  principal     = "apigateway.amazonaws.com"
}

resource "aws_lambda_permission" "auth_add_claim_lambda_permission-cognito" {
  statement_id  = "AllowCognitoInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.auth-add-claim-lambda.arn
  principal     = "cognito-idp.amazonaws.com"
  source_arn    = aws_cognito_user_pool.user-pool.arn
}

resource "aws_lambda_permission" "auth-lambda_permission-apigw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.auth-lambda.arn
  principal     = "apigateway.amazonaws.com"
}