# Define the AWS provider and specify the region
provider "aws" {
  region = "eu-central-1"                                   # Set the AWS region 
}

# Create an AWS Cognito User Pool
resource "aws_cognito_user_pool" "we-go-jim" {
  name                     = "we-go-jim"                    # Customize the user pool name here
  auto_verified_attributes = ["email"]                      # Set email as an attribute to verify(enables sending a verification email)
  mfa_configuration        = "OFF"                          # Set Multi-factor Authentification (MFA) configuration to "OFF" (can be "ON" or "OPTIONAL")

  # Define password policy for the user pool
  password_policy {
    minimum_length    = 8                                   # Minimum password length
    require_lowercase = true                                # Require at least one lowercase letter
    require_numbers   = true                                # Require at least one number
    require_symbols   = true                                # Require at least one symbol
    require_uppercase = true                                # Require at least one uppercase letter
  }

  # Specify username attributes and schema for the user pool
  username_attributes = ["email"]                           # Set the username attribute to "email"

  # Create a custom attribute
  schema {
    attribute_data_type      = "String"                     # Set attribute data type to String
    developer_only_attribute = false                        # 
    mutable                  = false                        # Set the attribute to unmodifiable 
    name                     = "user_type"                  # Set the name of the attribute
    required                 = false                        # Set the attribute to not required
                                                            # Has to be set up like that because Terraform 
                                                            # doesn't currently support setting custom attributes as required

    string_attribute_constraints {}                         # Set the attribute to have no constraints
  }

  email_configuration {
    email_sending_account = "COGNITO_DEFAULT"               # Set sending account as COGNITO_DEFAULT to stay in free tier
                                                            # However it can be modified
  }

  # Define verification message template for email confirmation
  verification_message_template {
    default_email_option    = "CONFIRM_WITH_LINK"                                                              # Set verification method as 
                                                                                                               # CONFIRM_WITH_LINK or CONFIRM_WITH_CODE               
    email_message_by_link   = "Please click the following link to verify your email address: {##Click Here##}" # Custom message body
    email_subject_by_link   = "Verify your email for We Go Jim"                                                # Custom subject
  }
}

# Create an AWS Cognito User Pool Client(necessary to use APIs)
resource "aws_cognito_user_pool_client" "we-go-jim-client" {
  name           = "we-go-jim-client"                        # Customize the client name here
  user_pool_id   = aws_cognito_user_pool.we-go-jim.id        # Get the user pool ID from resource reference
  generate_secret = true                                     # Generate the app client secret, necessary for user registration
  explicit_auth_flows = [
    "ALLOW_USER_PASSWORD_AUTH",                              # Allow user password authentication
     "ALLOW_REFRESH_TOKEN_AUTH"                              # Allow refresh token authentication
     ]          

}

# Create an AWS Cognito User Pool Domain(necessary to send verification link instead of a code)
 resource "aws_cognito_user_pool_domain" "we-go-jim-domain" {
  domain       = "we-go-jim"                                 # Customize the domain name here
  user_pool_id = aws_cognito_user_pool.we-go-jim.id          # Get the user pool ID from resource reference
}
