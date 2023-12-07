# Update these to your AWS configuration
$AWS_REGION = ''
$AWS_USER_POOL_ID = ''

$userList = aws cognito-idp list-users --region $AWS_REGION --user-pool-id $AWS_USER_POOL_ID | ConvertFrom-Json
$userList.Users | ForEach-Object {
    if ($_.UserStatus -like 'UNCONFIRMED'){
        aws cognito-idp admin-delete-user --region $AWS_REGION --user-pool-id $AWS_USER_POOL_ID --username $_.Username
    }  
}
