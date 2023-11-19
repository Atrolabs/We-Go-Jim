output "user_pool_id" {
  value = aws_cognito_user_pool.we-go-jim.id
}

output "user_pool_arn" {
  value = aws_cognito_user_pool.we-go-jim.arn
}

output "app_client_id" {
  value = aws_cognito_user_pool_client.we-go-jim-client.id
}

output "app_client_secret" {
  value = aws_cognito_user_pool_client.we-go-jim-client.client_secret
  sensitive = true
}
