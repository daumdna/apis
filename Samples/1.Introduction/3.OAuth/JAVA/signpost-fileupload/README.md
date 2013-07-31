OAuth 파일업로드(signpost) for Java
=============
본 샘플 코드는 Java에서 OAuth 인증 기반의 API인 블로그 API의 파일업로드을 사용해서 글과 함께 파일을 첨부하는 방법에 대해서 설명합니다. 

본 코드와 관련된 튜토리얼은 아래 링크에서 보실 수 있습니다.
[http://callback.dev.daum.net/apis/oauth/tutorial/java_signpost_fileupload](http://callback.dev.daum.net/apis/oauth/tutorial/java_signpost_fileupload)

>2013년 6월 27일 이후로 다음 요즘API가 종료되어 OAuth 파일 업로드 샘플코드는 블로그API를 사용한 코드로 변경되었습니다.
기존의 코드는 https://github.com/daumdna/apis/tree/master/Samples/5.Yozm/JAVA/fileUpload 에서 조회가능합니다. 
다음 요즘 API를 사용해 주신 여러분께 감사드립니다. 관련 공지: http://daumdna.tistory.com/779

##정보
* CreateDate : 2013/07/30
* Writer : 김주아
* Location : Samples/1.Introduction/3.OAuth/JAVA/signpost-fileupload
* Title : OAuth 인증 및 파일업로드
* Language : Java
* Using OpenAPI List

     1.https://apis.daum.net/oauth/requestToken

     2.https://apis.daum.net/oauth/authorize

     3.https://apis.daum.net/oauth/accessToken

     4.https://apis.daum.net/blog/post/uploadFile.do

     5.https://apis.daum.net/blog/post/write.do

* Using external library list

     1.[HttpClientt 4.1.1](http://hc.apache.org/downloads.cgi)

     2.[signpost-core-1.2.1.1.jar](http://code.google.com/p/oauth-signpost/downloads/detail?name=signpost-core-1.2.1.1.jar&can=2&q=)

     3.[signpost-commonshttp4-1.2.1.1.jar](http://code.google.com/p/oauth-signpost/downloads/detail?name=signpost-commonshttp4-1.2.1.1.jar&can=2&q=)
