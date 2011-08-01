<?php
// Request Token 요청 주소
$request_token_Url = 'https://apis.daum.net/oauth/requestToken';
// 사용자 인증 URL
$authorize_url = 'https://apis.daum.net/oauth/authorize';
// Access Token URL
$access_token_url = 'https://apis.daum.net/oauth/accessToken';

// Consumer 정보 (Consumer를 등록하면 얻어올 수 있음.)
$consumer_key = "[Consumer 등록을 한 후 각자 넣으세요.]";
$consumer_secret = "[Consumer 등록을 한 후 각자 넣으세요.]";
$callback_url = "[Consumer 등록을 한 후 각자 넣으세요.]";

// API prefix (보호된 자원이 있는 URL의 prefix)
$api_url = 'https://apis.daum.net';

// Service Provider와 통신할 인터페이스를 갖고 있는 객체 생성.
$oauth = new OAuth($consumer_key, $consumer_secret, OAUTH_SIG_METHOD_HMACSHA1, OAUTH_AUTH_TYPE_URI);
?>
