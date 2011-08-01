<?php
// Request Token 요청 주소
$request_token_url = 'https://apis.daum.net/oauth/requestToken';
// 사용자 인증 URL
$authorize_url = 'https://apis.daum.net/oauth/authorize';
// Access Token URL
$access_token_url = 'https://apis.daum.net/oauth/accessToken';

// Consumer 정보
$consumer_key = "{발급 받은 Consumer Key를 입력하세요.}";
$consumer_secret = "{발급 받은 Consumer Secret을 입력하세요.} ";
$callback_url = "{발급 받은 Callback URL을 입력하세요.}";

// API prefix
$api_url = "https://apis.daum.net";

// Service Provider와 통신할 인터페이스를 갖고 있는 객체 생성.
$oauth = new OAuth($consumer_key, $consumer_secret, OAUTH_SIG_METHOD_HMACSHA1, OAUTH_AUTH_TYPE_URI);
?>