resource "aws_cognito_user_pool" "user-pool" {
  name = "${var.projectName}-user-pool"

  auto_verified_attributes = ["email"]

  # Define as políticas de senha
  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
    require_uppercase = true
  }

  schema {
    name                = "name"
    attribute_data_type = "String"
    mutable             = true
    required            = true
  }

  schema {
    name                = "email"
    attribute_data_type = "String"
    mutable             = true
    required            = true
  }

  lambda_config {
    pre_token_generation = aws_lambda_function.auth-add-claim-lambda.arn
  }
}

resource "aws_cognito_user_pool_client" "user-pool-client" {
  name         = "${var.projectName}-user-pool-client"
  user_pool_id = aws_cognito_user_pool.user-pool.id

  explicit_auth_flows                  = ["ALLOW_USER_PASSWORD_AUTH", "ALLOW_USER_SRP_AUTH", "ALLOW_REFRESH_TOKEN_AUTH"]
  callback_urls                        = ["https://example.com/"]
  logout_urls                          = ["https://example.com/"]
  supported_identity_providers         = ["COGNITO"]
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_flows                  = ["code", "implicit"]
  allowed_oauth_scopes                 = ["openid", "email", "profile"]
  prevent_user_existence_errors        = "ENABLED"
}

resource "aws_cognito_user_pool_domain" "user-pool-domain" {
  domain       = "easyfood"
  user_pool_id = aws_cognito_user_pool.user-pool.id
}