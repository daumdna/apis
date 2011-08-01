using System.Collections.Generic;
using DevDefined.OAuth.Consumer;
using DevDefined.OAuth.Framework;

namespace Daum.Dna.OpenApi.Oauth.Test.Console
{
    class OAuthProgram
    {
        private static void Main()
        {
            string requestUrl = "https://apis.daum.net/oauth/requestToken";
            string userAuthorizeUrl = "https://apis.daum.net/oauth/authorize";
            string accessUrl = "https://apis.daum.net/oauth/accessToken";
            string callbackUrl = "oob";

            var consumerContext = new OAuthConsumerContext
            {
                //TODO:Daum OAuth소개 페이지(https://apis.daum.net/oauth/consumer/list)에서 등록된 Consumer 정보 입력
                ConsumerKey = "eb3eff10-b95d-455c-8572-e7858a2b34d0",
                ConsumerSecret = "suz6.HUjzlaG-S9ezBzFQ11FtKhQvv8cdT-9C_hWBFthpUmMTsOuUA00",
                SignatureMethod = SignatureMethod.HmacSha1,
            };

            //OAuth 준비
            var session = new OAuthSession(consumerContext, requestUrl, userAuthorizeUrl, accessUrl);
            session.WithQueryParameters(new Dictionary<string,string>(){ { "oauth_callback", callbackUrl } });
            
            // 1. request token 받기
            DevDefined.OAuth.Framework.IToken requestToken = session.GetRequestToken();

            // 인증주소 받기
            string authorizationLink = session.GetUserAuthorizationUrlForToken(requestToken, callbackUrl);

            // 2. 사용자 인증 하기
            System.Console.WriteLine("웹브라우저를 실행하여 다음 URL을 접속하세요.");
            System.Console.WriteLine(authorizationLink);
            System.Console.Write("\n\n웹브라우저에서 인증 후 반환 된 값을 입력하세요:");
            string inputVerifier = System.Console.ReadLine();

            // 얻어진 Verifier값을 포함시키기
            session.WithQueryParameters(new Dictionary<string, string>() { { "oauth_verifier", inputVerifier } });
            
            // 3. 인증 후 얻은 Verifier값을 이용하여 엑세스 토큰 얻기
            DevDefined.OAuth.Framework.IToken accessToken = session.ExchangeRequestTokenForAccessToken(requestToken);

            // '게시글 쓰기(한줄메모장)' API를 호출
            System.Console.WriteLine("OAuth를 통한 인증으로 '게시글 쓰기(한줄메모장)'를 호출하고 XML로 응답 받는 테스트를 합니다.");
            string apiUrl = "http://apis.daum.net/cafe/write_article/{cafeCode}/{boardId}.xml?";
            //{cafeCode} - 카페코드 : 
            //{boardId}
            apiUrl += string.Format("content={0}&", "여기는 메모를 삽입합니다.");
            apiUrl += string.Format("hideyn={0}&", "N"); //비밀글일때 Y
            
            string responseText = session.Request().Get().ForUrl(apiUrl).ToString();

            System.Console.WriteLine(responseText);
            System.Console.ReadLine();
        }
    }
}
