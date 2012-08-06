var util = require('util');
var OAuth = require('oauth').OAuth;
var read = require('read');

// 1. Provider 정보 설정
var requestTokenUrl = "https://apis.daum.net/oauth/requestToken";
var authorizeUrl = "https://apis.daum.net/oauth/authorize";
var accessTokenUrl = "https://apis.daum.net/oauth/accessToken";

// 2. 컨슈머 정보 설정
var consumerKey = "cfd28df5-9e98-4e72-8b2c-052b9b663afd";
var consumerSecret = "Ps5fbgtu6SxGfYJGwt_6jilpKfMoTFtXKhTq_BPoiEYaDyqhROn2nA00";
var callbackUrl = "oob";

var consumer = new OAuth(
            requestTokenUrl, accessTokenUrl, 
            consumerKey, consumerSecret, "1.0", callbackUrl, "HMAC-SHA1");   


// 3. Request Token 요청
consumer.getOAuthRequestToken(function(err, token, tokenSecret, results) {
  if (err) {
    console.log(err);
  } else {
    requestToken = token;
    requestTokenSecret = tokenSecret;

	// 4. 사용자 로그인
    console.log(authorizeUrl + "?oauth_token=" + requestToken);
    console.log("웹브라우저에서 위 URL로 가서 인증코드를 얻고 입력하세요.");

	// 5. verifier 입력 받기
    read({prompt: "verifier: "}, function(err, verifier) {
      if(err) {
		console.log(err);
      } else {

		// 6. Request Token을 AccessToken 으로 교환
		consumer.getOAuthAccessToken(requestToken, requestTokenSecret, verifier, function(err, accessToken, accessTokenSecret, result) {
		  if (err) {
		    console.log(err);
		  } else {

		    console.log("Access Token = " + accessToken);
		    console.log("Access Token Secret = " + accessTokenSecret);

		 	// 7. 보호된 자원에 접근
			var params = {buddyId:"PU_oVHcH-8VRRY0", content:"테스트"};
			var resourceUrl = "https://apis.daum.net/cafe/favorite_cafes.json";
			consumer.post(resourceUrl, accessToken, accessTokenSecret, params, null, function(err, data, res) {
			  if(err) {
			    console.log(err);
			  } else {
			    console.log(data)
			  }
			});
		  }
		});
 	 }
 	});
 }
});