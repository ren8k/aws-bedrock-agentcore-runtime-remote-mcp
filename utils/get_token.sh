# AWS CLIでテスト用のトークンを取得
aws cognito-idp initiate-auth \
  --auth-flow USER_PASSWORD_AUTH \
  --client-id uc042nrsh6ip4vtqbkd4pj1hb \
  --auth-parameters USERNAME=testuser,PASSWORD=MyPassword123!
