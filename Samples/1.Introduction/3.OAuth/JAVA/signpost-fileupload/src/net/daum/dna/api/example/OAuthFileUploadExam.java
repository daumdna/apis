package net.daum.dna.api.example;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.UnsupportedEncodingException;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import oauth.signpost.OAuth;
import oauth.signpost.OAuthConsumer;
import oauth.signpost.OAuthProvider;
import oauth.signpost.basic.DefaultOAuthProvider;
import oauth.signpost.commonshttp.CommonsHttpOAuthConsumer;
import oauth.signpost.exception.OAuthCommunicationException;
import oauth.signpost.exception.OAuthExpectationFailedException;
import oauth.signpost.exception.OAuthMessageSignerException;
import oauth.signpost.exception.OAuthNotAuthorizedException;

import org.apache.http.HttpEntity;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.mime.MultipartEntity;
import org.apache.http.entity.mime.content.FileBody;
import org.apache.http.entity.mime.content.StringBody;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.xml.sax.SAXException;

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

	public static void main(String[] args) throws OAuthMessageSignerException, OAuthNotAuthorizedException,
			OAuthExpectationFailedException, OAuthCommunicationException, ClientProtocolException, IOException,
			ParserConfigurationException, SAXException {
		String authUrl = provider.retrieveRequestToken(consumer, OAuth.OUT_OF_BAND);

		System.out.println("아래 URL로 가서 사용자 인증을 하시면 인증코드(verifier)를 얻을 수 있습니다.");
		System.out.println(authUrl);

		System.out.print("인증코드 입력 : ");
		Scanner s = new Scanner(System.in);
		String verifier = s.next();

		provider.retrieveAccessToken(consumer, verifier);

		/*
		 * // 여기서는 변수에 저장하지만, 실제로 개발을 할 때는 Access Token이 발급된 이후, 
		 * // FileSystem,DB 등 저장공간에 넣어두고, 이후에는 발급절차를 생략할 수 있다.
		 * 
		 * final String ACCESS_TOKEN = consumer.getToken(); final String
		 * TOKEN_SECRET TOKEN_SECRET = consumer.getTokenSecret();
		 * 
		 * 
		 * // 미리 저장된 Access token 정보는 setTokenWithSecret() 메소드로 지정할 수 있다.
		 * consumer.setTokenWithSecret(ACCESS_TOKEN, TOKEN_SECRET);
		 */

		File file = new File("C:\\temp\\daumlogo.png"); // 첨부할 파일
		String fileUrl = uploadFile(file); // 파일 업로드 후 파일주소 리턴
		writeArticleWithFile(fileUrl, file.getName(), file.length()); // 파일첨부하여 새 글 쓰기

	}

	public static String uploadFile(File file) {
		String fileUrl = "";
		try {
			// 블로그 파일업로드 API의 URL 지정
			HttpPost uploadFile = new HttpPost(API_URL + "/blog/post/uploadFile.do");

			// uploadPost 서명 (oauth_signature 파라미터 생성됨)
			consumer.sign(uploadFile);

			// 요청 형식이 multipart/form-data 인경우에
			// POST body의 내용은 oauth_signature를 만드는데 사용되지 않음으로 서명 이후 추가
			MultipartEntity entity = new MultipartEntity();

			// 블로그명, 파일 데이터,
			StringBody blogName = new StringBody("[블로그명을 입력하세요(http://blog.daum.net/블로그명)]", Charset.forName("UTF-8"));
			FileBody imgData = new FileBody(file, "image/png");
			entity.addPart("blogName", blogName);
			entity.addPart("img_data", imgData);
			uploadFile.setEntity(entity);

			// API 호출 (파일을 전송)
			DefaultHttpClient httpClient = new DefaultHttpClient();
			HttpEntity httpEntitiy = httpClient.execute(uploadFile).getEntity();
			InputStream inputStream = httpEntitiy.getContent();

			fileUrl = retrieveFileUrl(inputStream);
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			System.out.println("--------------파일업로드 결과--------------");
			System.out.println("업로드 된 파일주소 : " + fileUrl);
		}
		return fileUrl;

	}

	private static String retrieveFileUrl(InputStream inputStream) {
		StringBuffer sb = new StringBuffer("");
		try {
			//DOM객체로 만들기
			DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
			DocumentBuilder builder = factory.newDocumentBuilder();
			Document doc = builder.parse(inputStream);

			// 파싱하기
			Node channelNode = doc.getElementsByTagName("channel").item(0);
			for (int i = 0; i < channelNode.getChildNodes().getLength(); i++) {
				Node node = channelNode.getChildNodes().item(i);
				String nodeName = node.getNodeName();
				if (nodeName.equals("status")) {
					if (!node.getTextContent().equals("200"))
						break;		//응답코드가 200(성공)이 아닐경우 파싱종료
				} else if (nodeName.equals("url")) {
					sb.append(node.getTextContent());
					break;
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		return sb.toString();
	}

	private static void writeArticleWithFile(String fileUrl, String fileName, long fileSize) 
	{
		try {
			DefaultHttpClient httpClient = new DefaultHttpClient();
			if (!fileUrl.equals("")) {
				HttpPost writeArticle = new HttpPost(API_URL + "/blog/post/write.do");
	
				List<NameValuePair> params = new ArrayList<NameValuePair>();
				params.add(new BasicNameValuePair("blogName", "bigbanggirl"));
				params.add(new BasicNameValuePair("title", "글 제목"));
				params.add(new BasicNameValuePair("content", "글 본문"));
				params.add(new BasicNameValuePair("fileUrl", fileUrl));
				params.add(new BasicNameValuePair("fileName", fileName));
				params.add(new BasicNameValuePair("fileType", "im"));
				params.add(new BasicNameValuePair("fileSize", String.valueOf(fileSize)));
				UrlEncodedFormEntity paramEntity = new UrlEncodedFormEntity(params, "UTF-8");
				writeArticle.setEntity(paramEntity);
	
				consumer.sign(writeArticle);
				System.out.println("--------------파일첨부하여 새 글쓰기 결과--------------");
				System.out.println(httpClient.execute(writeArticle, new BasicResponseHandler()));
			}
		}
		catch (Exception e) {
			e.printStackTrace();	
		}
	}
}
