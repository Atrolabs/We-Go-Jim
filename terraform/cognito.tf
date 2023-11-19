provider "aws" {
  region = "eu-central-1"
}

resource "aws_cognito_user_pool" "we-go-jim" {
  name = "we-go-jim"

  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
    require_uppercase = true
  }

  username_attributes = ["email"]

  schema {
    attribute_data_type = "String"
    name               = "user_type"
    required           = false
  }

  auto_verified_attributes = ["email"]
  email_verification_subject = "Verify your email for We Go Jim"
  email_verification_message = "Please click the following link to verify your email address: {####}"

  mfa_configuration = "OFF"
}
