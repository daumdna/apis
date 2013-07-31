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
		.apiKey("[Consumer 등록후 Key를 입력하세요]")
		.apiSecret("[Consumer 등록후 Secret Key를 입력하세요]")
		.callback("oob")
		.build();

		Scanner in = new Scanner(System.in);
		
		// 1. request token 받기
	    Token requestToken = service.getRequestToken();

	    // 2. 사용자 인증 하기
	    System.out.println("웹브라우저를 실행하여 다음 URL을 접속하세요.");
	    System.out.println(service.getAuthorizationUrl(requestToken) + "?" + requestToken.getRawResponse());
	    System.out.print("웹브라우저에서 인증 후 반환 된 값을 입력하세요:");
	    Verifier verifier = new Verifier(in.nextLine());
	    System.out.println();

	    // 3. 인증 후 얻은 Verifier값을 이용하여 엑세스 토큰 얻기
	    Token accessToken = service.getAccessToken(requestToken, verifier);
	    
	    // '프로필 정보 조회 API를 통해 인증 확인하기
	    OAuthRequest request = new OAuthRequest(Verb.GET, "https://apis.daum.net/profile/show.xml");
	    service.signRequest(accessToken, request);
	    Response response = request.send();
	    System.out.println(response.getBody());
	    System.out.println();
	}

}
