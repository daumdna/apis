# OAuth 기본 튜토리얼 for Node.js
===
이 튜토리얼에서는 [Node.js](http://nodejs.org)를 이용한 OAuth 인증 기반의 API를 사용하는 방법에 대해서 설명합니다. 

## 요구사항

  - [Node.js](http://nodejs.org/) 코딩 능력
  - [OAuth의 기본적인 이해](http://dna.daum.net/apis/oauth/intro)

## 일단 실행해보기

관련 모듈 설치:

    npm install

실행하기:
    
    node oauth_console.js

# 튜토리얼
---

## Consumer 등록
우선 [Consumer 등록](https://apis.daum.net/oauth/consumer/input)부터 하세요. 그러면 Consumer Key/Secret을 얻을 수 있습니다.

> "Consumer의 형태는 웹서비스와 일반 애플리케이션이 있을 수 있는데, 여기서 우리는 일반 애플리케이션을 만들 예정입니다. 일반 애플리케이션은 Callback URL이 필요 없습니다."

## 소스코드

이제 직접 코딩을 해보도록 하겠습니다. OAuth 인증을 통한 보호된 자원을 얻는 절차는 아래와 같고, 그 순서에 따라 코드를 작성해 보겠습니다.

1. URL 및 Consumer 정보 설정
2. **Request Token 요청**
3. **사용자 인증(Authentication) 및 권한 위임(Authorization)**
4. Verifier(인증코드) 입력받기
5. **Request Token을 Access Token으로 교환**
6. Access Token을 싣고 API 호출하면, 보호된 자원으로 접근

OAuth에서는 3가지 중요한 URL이 있는데, Daum OAuth에서는 아래와 같은 URL을 사용합니다.

#### Request Token 요청
 
    https://apis.daum.net/oauth/requestToken

#### 사용자 인증 URL

    https://apis.daum.net/oauth/authorize

#### Access Token URL

    https://apis.daum.net/oauth/accessToken

보시면 아시겠지만 이 URL들은 각각 위에서 설명했던 굵게 표시된 OAuth 인증 절차 부분에서 사용됩니다.

> "간혹, 저 URL을 웹브라우저에서 그대로 쳐서 왜 에러만 나고 안 되냐고 문의하시는 분들이 계신데, 각 단계마다 알맞는 파라미터를 붙여서 호출해야 합니다. 각 단계별 파라미터에 대한 내용은 [OAuth 공식 사이트에 잘 나와 있습니다.](http://oauth.net/core/1.0a/) 그러나 [OAuth 라이브러리 사용법](http://oauth.net/code/)만 익히면 오가는 파라미터에 대해서 정확히 알지 못해도 OAuth인증을 구현하실 수 있습니다."

### 1. URL 및 Consumer 정보 설정

우선 config.js를 만들어 보겠습니다. 전체 코드는 아래와 같습니다. 여기에서 URL과 Consumer에 대한 정보들을 설정합니다.

#### config.js
    // 1. URL 및 Consumer 정보 설정
    var config = {
      requestTokenUrl: "https://apis.daum.net/oauth/requestToken",
      authorizeUrl: "https://apis.daum.net/oauth/authorize",
      accessTokenUrl: "https://apis.daum.net/oauth/accessToken",
      consumerKey: "[Consumer 등록 후 각자 입력하세요]",
      consumerSecret: "[Consumer 등록 후 각자 입력하세요]",
      callbackUrl: "oob"
    }

    // 외부 모듈에 사용할 수 있도록 export
    exports.config = config;

코드를 단계적으로 자세히 살펴보겠습니다. 우선 설정 정보를 저장할 config 객체를 만듭니다.

    var config = {};

아래와 같이 URL을 설정합니다.

    var config = {
      requestTokenUrl: "https://apis.daum.net/oauth/requestToken",
      authorizeUrl: "https://apis.daum.net/oauth/authorize",
      accessTokenUrl: "https://apis.daum.net/oauth/accessToken"
    }

그리고 [Consumer 등록](https://apis.daum.net/oauth/consumer/input)을 통해 얻은 Consumer Key/Secret, Callback URL 정보도 지정합니다. 일반 애플리케이션의 경우 Callback URL *oob*라는 문자열을 사용합니다.

    // 1. URL 및 Consumer 정보 설정
    var config = {
      requestTokenUrl: "https://apis.daum.net/oauth/requestToken",
      authorizeUrl: "https://apis.daum.net/oauth/authorize",
      accessTokenUrl: "https://apis.daum.net/oauth/accessToken",
      consumerKey: "[Consumer 등록 후 각자 입력하세요]",
      consumerSecret: "[Consumer 등록 후 각자 입력하세요]",
      callbackUrl: "oob"
    }

    // 외부 모듈에 사용할 수 있도록 export
    exports.config = config;


> "이 튜토리얼이 완성된 후에 OAuth 인증을 지원하는 다른 Service Provider([Google](http://code.google.com/intl/ko-KR/apis/accounts/docs/OAuth.html), [Twitter](http://dev.twitter.com/pages/auth) 등)로 바꿀 경우에는 이 URL 값과 Consumer 정보만 수정하고, 호출하는 API 주소 정도만 바꾸면 됩니다."

다음에는 설정한 정보를 바탕으로 본격적으로 OAuth 절차를 밟기 위해 app.js를 만듭니다. 이 때 방금전 설정한 config를 사용하기 위해 ./config를 require하고, OAuth 사용을 위해 oauth 모듈을, 키보드 입력을 받기 위해 read 모듈을 require 합니다.

    var config = require('./config').config,
      OAuth = require('oauth').OAuth,
      read = require('read');
  
    // Service Provider와 통신할 인터페이스를 갖고 있는 객체 생성.
    var oauth = new OAuth(
                config.requestTokenUrl, config.accessTokenUrl, 
                config.consumerKey, config.consumerSecret,
                "1.0", config.callbackUrl, "HMAC-SHA1");

> "OAuth 객체 생성시 OAUTH_SIG_METHOD_HMACSHA1 이라는 것은 서명 메소드가 HMAC-SHA1이라는 것을 의미합니다. Daum OAuth는 HMAC-SHA1만 지원하므로 그냥 이렇게 사용하면 된다고 아시면 됩니다."

### 2. Request Token 요청
이번에는 Service Provider에 Request Token을 요청합니다.

#### app.js
    oauth.getOAuthRequestToken(function(err, requestToken, requestTokenSecret, results) {
      if (err) {
        console.log(err);
      } else {
        중략...
      }
    });

미리 생성한 oauth객체의 메소드인 getOAuthRequestToken 호출을 통해 Request Token을 얻을 수 있습니다. 이 때 결과는 Node.js의 특성 답게 callback 함수에서 얻을 수 있습니다. 그리고 이 callback 함수 내부(중략... 이라고 된 부분)에서 계속 다음 단계로 넘어가는 형식을 취합니다.

### 3. 사용자 인증(Authentication) 및 권한 위임(Authorization)

Request Token/Secret은 이후에 Access Token으로 변경됩니다. 아래 코드와 같이 사용자 인증 URL에 token을 쿼리스트링 으로 만든 URL로 사용자가 웹브라우저에서 보도록 합니다. 지금은 콘솔 프로그램이어서 사용자가 웹브라우저에 해당 URL을 직접 붙여 넣어야 하지만, 웹프로그램이라면 그냥 redirect 시켜주면 되겠죠?

    // 3. 사용자 인증(Authentication) 및 권한 위임(Authorization)
    console.log(config.authorizeUrl + "?oauth_token=" + requestToken);
    console.log("웹브라우저에서 위 URL로 가서 인증코드를 얻고 입력하세요.");

이 때 사용자가 로그인이 안 되어 있으면 Daum의 로그인 페이지가 나와서 로그인을 유도합니다. 로그인이 끝나면, 사용자는 아래와 같은 형태의 화면을 보게 되고 해당 컨슈머에게 권한을 위임할지 결정하게 합니다.

![사용자에게 권한 위임 승인 여부를 묻는 화면](http://cfile25.uf.tistory.com/image/183B9337501B930325210A)

### 4. Verifier(인증코드) 입력받기

사용자가 사용자 인증 URL로 가서 로그인 및 권한 위임을 승인하면 verifier(인증코드)를 얻게 됩니다. 그리고 사용자는 그 코드 값을 직접 입력하게 됩니다.

    // 4. verifier 입력 받기
    read({prompt: "verifier: "}, function(err, verifier) {
      if(err) {
        console.log(err);
      } else {
        중략...
      }
    }


> "이때, 컨슈머 등록시 서비스형태를 웹서비스로 선택했으면 지정했던 Callback URL로 넘어 갑니다. 그리고 그 Callback URL의 Query String으로 verifier(oauth_verifier)를 넘겨줍니다."

### 5. Request Token을 Access Token으로 교환

이제 Request Token은 Access Token으로 교환하게 됩니다. 이 때 verifier(인증코드) 값과 Request Token 조합으로 Access Token을 얻어냅니다. 아래과 같은 형태로 구현이 될 수 있습니다.

    // 5. Request Token을 AccessToken 으로 교환
    oauth.getOAuthAccessToken(requestToken, requestTokenSecret, verifier, function(err, accessToken, accessTokenSecret, result) {
      if (err) {
        console.log(err);
      } else {
  
        console.log("Access Token = " + accessToken);
        console.log("Access Token Secret = " + accessTokenSecret);
  
        중략...
      }
    });

> "여기서는 편의상 변수에 저장하지만 실서비스 개발 시에는 Access Token이 발급된 이후, FileSystem, DB 등 저장공간에 넣어두고, 이후에는 발급절차를 생략할 수 있습니다."


### 6. Access Token을 싣고 API 호출하면, 보호된 자원으로 접근
  
이제 Access Token을 얻었으므로 컨슈머는 사용자로부터 그 사용자의 보호된 자원에 접근할 수 있는 권한을 위임 받은 것입니다. 그러므로 이제는 사용자가 직접 로그인 하지 않아도 컨슈머가 필요할 때 보호된 자원에 접근할 수 있습니다.

> "Access Token은 영구적이지 않습니다. 일단 만료 기간(Daum은 1년)이 있습니다. 그럴 경우 "token expired" 에러가 떨어집니다. 그리고 사용자가 언제든지 Access Token을 삭제할 수도 있습니다. Daum의 경우 <a href="http://profile.daum.net">Daum 프로필</a> 서비스에서 Access Token을 삭제할 수 있는 기능을 제공합니다. 따라서 실서비스에서 구현할 때는 보호된 자원 접근시 token expired, token rejected 명령이 떨어질 수 있고 이런 에러가 떨어지면 다시 처음으로 돌아가서 Access Token을 발급 받을 수 있도록 개발해야 합니다."

캘린더 API 뿐 아니라 다른 API들도 각 레퍼런스를 참조해서 같은 방법으로 모두 구현하실 수 있습니다.

    // 6. 보호된 자원에 접근
    var resourceUrl = config.apiUrl + "/calendar/category/index.json";
    oauth.get(resourceUrl, accessToken, accessTokenSecret, function(err, data, res) {
      if(err) {
        console.log(err);
      } else {
        categories = eval(data);
  
        for(var i = 0; i &lt; categories.length; i++) {
          console.log(categories[i].name);
        }
      }
    });

이렇게 해서 우리는 OAuth 인증 기반으로 Access Token을 발급 받고, API를 호출해서 보호된 자원을 얻어오는 일까지 모두 성공했습니다.

## 다운로드
 - [다운로드 (github)](https://github.com/daumdna/apis/tree/master/Samples/1.Introduction/3.OAuth/Javascript/nodejs)

참고자료
---
  - [OAuth 시작하기](https://dna.daum.net/apis/oauth)
  - [OAuth 기본 튜토리얼 for Node.js](https://dna.daum.net/apis/oauth/tutorial/nodejs)
  - [nodejs.org](http://nodejs.org/)
  - [how to install node.js and npm (node package manager)](http://joyeur.com/2010/12/10/installing-node-and-npm/)