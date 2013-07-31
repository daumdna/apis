package net.daum.dna.api.example;

import java.io.File;
import java.nio.charset.Charset;
import java.util.Scanner;

import oauth.signpost.OAuth;
import oauth.signpost.OAuthConsumer;
import oauth.signpost.OAuthProvider;
import oauth.signpost.basic.DefaultOAuthProvider;
import oauth.signpost.commonshttp.CommonsHttpOAuthConsumer;
import oauth.signpost.exception.OAuthCommunicationException;
import oauth.signpost.exception.OAuthExpectationFailedException;
import oauth.signpost.exception.OAuthMessageSignerException;
import oauth.signpost.exception.OAuthNotAuthorizedException;

import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.mime.MultipartEntity;
import org.apache.http.entity.mime.content.FileBody;
import org.apache.http.entity.mime.content.StringBody;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient;

public class OAuthFileUploadExam {
	static final String REQUEST_TOKEN_URL = "https://apis.daum.net/oauth/requestToken"; 
    static final String AUTHORIZE_URL = "https://apis.daum.net/oauth/authorize";
    static final String ACCESS_TOKEN_URL = "https://apis.daum.net/oauth/accessToken";
    
    static final String CONSUMER_KEY = "[Consumer 등록을 한 후 각자 넣으세요.]";
    static final String CONSUMER_SECRET = "[Consumer 등록을 한 후 각자 넣으세요.]";
    
    // API prefix (보호된 자원이 있는 URL의 prefix)
    static final String API_URL = "https://apis.daum.net";

    // Service Provider 객체 생성
    static OAuthProvider provider = new DefaultOAuthProvider(REQUEST_TOKEN_URL, ACCESS_TOKEN_URL, AUTHORIZE_URL);   
    // Consumer 객체 생성
    static OAuthConsumer consumer = new CommonsHttpOAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET);

    public static void uploadFile(File file) {
    	try {
			// 요즘 글쓰기 API의 URL 지정
			HttpPost uploadPost = new HttpPost(API_URL + "/yozm/v1_0/message/add.xml");
		
			// uploadPost 서명 (oauth_signature 파라미터 생성됨)
			consumer.sign(uploadPost);
			
			// 요청 형식이 multipart/form-data 인경우에
			// POST body의 내용은 oauth_signature를 만드는데 사용되지 않음으로 서명 이후 추가
			MultipartEntity entity = new MultipartEntity();

			// 파일 데이터, yozm 글 내용 추가
			FileBody imgData = new FileBody(file, "image/jpeg");
			StringBody message = new StringBody("파일업로드 테스트~!", Charset.forName("UTF-8"));
			entity.addPart("img_data", imgData);
			entity.addPart("message", message);
			
			uploadPost.setEntity(entity);
			
			// API 호출 (파일과 메시지를 보낸다.)
			DefaultHttpClient httpClient = new DefaultHttpClient();
			System.out.println(httpClient.execute(uploadPost, new BasicResponseHandler()));
			
		} catch (Exception e) {
		     e.printStackTrace();
		}
    }
       
	public static void main(String[] args) throws OAuthMessageSignerException, OAuthNotAuthorizedException, OAuthExpectationFailedException, OAuthCommunicationException {		
		String authUrl = provider.retrieveRequestToken(consumer, OAuth.OUT_OF_BAND);
		 
        System.out.println("아래 URL로 가서 사용자 인증을 하시면 인증코드(verifier)를 얻을 수 있습니다.");
        System.out.println(authUrl);
        
        System.out.print("인증코드 입력 : ");
        Scanner s = new Scanner(System.in);             
        String verifier = s.next();
        
        provider.retrieveAccessToken(consumer, verifier);
        
/*
        // 여기서는 변수에 저장하지만, 실제로 개발을 할 때는 Access Token이 발급된 이후,
        // FileSystem, DB 등 저장공간에 넣어두고, 이후에는 발급절차를 생략할 수 있다. 
                
        final String ACCESS_TOKEN = consumer.getToken();
        final String TOKEN_SECRET = consumer.getTokenSecret();
                        
        
        // 미리 저장된 Access token 정보는 setTokenWithSecret() 메소드로 지정할 수 있다.
        consumer.setTokenWithSecret(ACCESS_TOKEN, TOKEN_SECRET);
*/              
		File file = new File("C:\\temp\\daum_logo.jpg");
		uploadFile(file);
	}
}
