using System.Collections.Generic;
using DevDefined.OAuth.Consumer;
using DevDefined.OAuth.Framework;

namespace Daum.Dna.OpenApi.Oauth.Test.Console
{
    class Program
    {
        private static void Main()
        {
            string requestUrl = "https://apis.daum.net/oauth/requestToken";
            string userAuthorizeUrl = "https://apis.daum.net/oauth/authorize";
            string accessUrl = "https://apis.daum.net/oauth/accessToken";
            string callBackUrl = "oob";

            var consumerContext = new OAuthConsumerContext
            {
                //TODO:Daum OAuth소개 페이지(https://apis.daum.net/oauth/consumer/list)에서 등록된 Consumer 정보 입력
                ConsumerKey = "{발급 받은 Key를 입력하세요.}",
                ConsumerSecret = "{발급 받은 Secret를 입력하세요.}",
                SignatureMethod = SignatureMethod.HmacSha1,
            };

            //OAuth 준비
            var session = new OAuthSession(consumerContext, requestUrl, userAuthorizeUrl, accessUrl);
            session.WithQueryParameters(new Dictionary<string,string>(){ { "oauth_callback", callBackUrl } });
            
            // 1. request token 받기
            DevDefined.OAuth.Framework.IToken requestToken = session.GetRequestToken();

            // 인증주소 받기
            string authorizationLink = session.GetUserAuthorizationUrlForToken(requestToken, callBackUrl);

            // 2. 사용자 인증 하기
            System.Console.WriteLine("웹브라우저를 실행하여 다음 URL을 접속하세요.");
            System.Console.WriteLine(authorizationLink);
            System.Console.Write("\n\n웹브라우저에서 인증 후 반환 된 값을 입력하세요:");
            string inputVerifier = System.Console.ReadLine();

            // 얻어진 Verifier값을 포함시키기
            session.WithQueryParameters(new Dictionary<string, string>() { { "oauth_verifier", inputVerifier } });
            
            // 3. 인증 후 얻은 Verifier값을 이용하여 엑세스 토큰 얻기
            DevDefined.OAuth.Framework.IToken accessToken = session.ExchangeRequestTokenForAccessToken(requestToken);

            // '요즘 가입여부 확인하기' API를 통해 인증 확인하기
            System.Console.WriteLine("OAuth를 통한 인증으로 '요즘 가입여부 확인하기'를 테스트합니다.");
            string responseText = session.Request().Get().ForUrl("https://apis.daum.net/yozm/v1_0/user/joined.xml?").ToString();

            System.Console.WriteLine(responseText);
            System.Console.ReadLine();
        }
    }
}
