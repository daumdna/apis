<?php
// Request Token ��û �ּ�
$request_token_url = 'https://apis.daum.net/oauth/requestToken';
// ����� ���� URL
$authorize_url = 'https://apis.daum.net/oauth/authorize';
// Access Token URL
$access_token_url = 'https://apis.daum.net/oauth/accessToken';

// Consumer ��� (Consumer�� ����ϸ� ���� �� ���.)
$consumer_key = "[Consumer ���� �� �� ���� �������.]";
$consumer_secret = "[Consumer ���� �� �� ���� �������.]";
$callback_url = "[Consumer ���� �� �� ���� �������.]";

// API prefix (��ȣ�� �ڿ��� �ִ� URL�� prefix)
$api_url = 'https://apis.daum.net';

// Service Provider�� ����� �������̽��� ���� �ִ� ��ü ��.
$oauth = new OAuth($consumer_key, $consumer_secret, OAUTH_SIG_METHOD_HMACSHA1, OAUTH_AUTH_TYPE_URI);
?>
