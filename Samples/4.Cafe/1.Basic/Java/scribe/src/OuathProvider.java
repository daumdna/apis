package net.daum.dna.api.example;

import java.util.Scanner;

import org.scribe.builder.ServiceBuilder;
import org.scribe.model.OAuthRequest;
import org.scribe.model.Response;
import org.scribe.model.Token;
import org.scribe.model.Verb;
import org.scribe.model.Verifier;
import org.scribe.oauth.OAuthService;

public class OuathProvider {
	public static void main(String[] args) {
		//OAuth 준비
		OAuthService service = new ServiceBuilder()
		.provider(DaumDnaApi.class)
		.apiKey("[Consumer 등록을 한 후 각자 넣으세요.]")
		.apiSecret("[Consumer 등록을 한 후 각자 넣으세요.]")
		.callback("oob") //콘솔이므로 oob로 지정
		.build();

		Scanner in = new Scanner(System.in);
		
		// 1. request token 받기
	    Token requestToken = service.getRequestToken();

	    // 2. 사용자 인증 하기
	    System.out.println("아래 URL로 가서 사용자 인증을 하시면 인증코드(verifier)를 얻을 수 있습니다.");
	    System.out.println(service.getAuthorizationUrl(requestToken) + "?" + requestToken.getRawResponse());
	    System.out.print("인증코드 입력 :");
	    Verifier verifier = new Verifier(in.nextLine());
	    System.out.println();

	    // 3. 인증 후 얻은 Verifier값을 이용하여 엑세스 토큰 얻기
	    Token accessToken = service.getAccessToken(requestToken, verifier);
	    
	    // '요즘 가입여부 확인하기' API를 통해 인증 확인하기
	    OAuthRequest request = new OAuthRequest(Verb.GET, "http://apis.daum.net/cafe/write_article/{cafeCode}/{boardId}.xml?");
	    request.addQuerystringParameter("content", "여기는 메모를 삽입합니다.");
	    request.addQuerystringParameter("hideyn", "N"); //비밀글일때 Y
	    service.signRequest(accessToken, request);
	    Response response = request.send();
	    System.out.println(response.getBody());
	    System.out.println();
	}

}
