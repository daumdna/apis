using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net;
using System.IO;
using System.Xml.Serialization;
using System.Collections.Specialized;

namespace Daum.Dna.OpenApi.Samples.Blog
{
    class FileUploader
    {
        //TODO:할당받은 컨슈머키와 컨슈머 시크릿을 포함 하여 OAuth 관리개체 생성
        private static OAuth.Manager _oauth = new OAuth.Manager("[발급 받은 Key를 입력하세요.]", "[발급 받은 Secret를 입력하세요.]", "", "");

        static void Main(string[] args)
        {
            // 1. request token 받기
            var response1 = _oauth.AcquireRequestToken("https://apis.daum.net/oauth/requestToken", "POST");

            // 인증주소 받기
            var uriString = "https://apis.daum.net/oauth/authorize?oauth_token=" + response1["oauth_token"];

            // 2. 사용자 인증 하기
            System.Console.WriteLine("웹브라우저를 실행하여 다음 URL을 접속하세요.");
            System.Console.WriteLine(uriString);
            System.Console.Write("\n\n웹브라우저에서 인증 후 반환 된 값을 입력하세요:");
            string inputVerifier = System.Console.ReadLine();

            // 3. 인증 후 얻은 Verifier값을 이용하여 엑세스 토큰 얻기
            var response2 = _oauth.AcquireAccessToken("https://apis.daum.net/oauth/accessToken", "POST", inputVerifier);

            //얻은 토큰을 관리개체에 포함
            _oauth["token"] = response2["oauth_token"];
            _oauth["token_secret"] = response2["oauth_token_secret"];

            string url = "http://apis.daum.net/blog/post/uploadFile.do?blogName=블로그명을입력하세요";

            //전송할 인증정보를 헤더에 넣어야 하므로 헤더정보 생성
            var authzHeader = _oauth.GenerateAuthzHeader(url, "POST");

            //헤더 정보와 url, 파일정보를 포함하여 전송후 출력된 정보 반환
            string ret = UploadFilesToRemoteUrl(url, new string[] { "C:\\temp\\daumlogo.png" }, authzHeader);

            System.Console.WriteLine(ret);
        }

        /// <summary>
        /// 업로드 *예외처리 안되어 있음
        /// </summary>
        /// <param name="url">업로드 주소</param>
        /// <param name="files">업로드 파일주소들</param>
        /// <param name="authzHeader">인증헤더 정보</param>
        public static string UploadFilesToRemoteUrl(string url, string[] files, string authzHeader)
        {

            string boundary = "----------------------------" + DateTime.Now.Ticks.ToString("x");

            HttpWebRequest httpWebRequest2 = (HttpWebRequest)WebRequest.Create(url);
            httpWebRequest2.Method = "POST";
            httpWebRequest2.PreAuthenticate = true;
            httpWebRequest2.AllowWriteStreamBuffering = true;
            //중요) 헤더를 Authorization키로 하여 삽입 
            httpWebRequest2.Headers.Add("Authorization", authzHeader);
            httpWebRequest2.ContentType = "multipart/form-data; boundary=" + boundary;

            Stream memStream = new System.IO.MemoryStream();

            byte[] boundarybytes = System.Text.Encoding.ASCII.GetBytes("\r\n--" + boundary + "\r\n");
            string formdataTemplate = "\r\n--" + boundary + "\r\nContent-Disposition: form-data; name=\"{0}\";\r\n\r\n{1}";

            memStream.Write(boundarybytes, 0, boundarybytes.Length);
            string headerTemplate = "Content-Disposition: form-data; name=\"{0}\"; filename=\"{1}\"\r\n Content-Type: application/octet-stream\r\n\r\n";

            for (int i = 0; i < files.Length; i++)
            {
                string header = string.Format(headerTemplate, "uplTheFile", files[i]);
                byte[] headerbytes = System.Text.Encoding.UTF8.GetBytes(header);
                memStream.Write(headerbytes, 0, headerbytes.Length);

                if (File.Exists(files[i]) == false) throw new Exception(files[i] + "파일이 없습니다.");

                FileStream fileStream = new FileStream(files[i], FileMode.Open, FileAccess.Read);
                byte[] buffer = new byte[1024];
                int bytesRead = 0;
                while ((bytesRead = fileStream.Read(buffer, 0, buffer.Length)) != 0)
                    memStream.Write(buffer, 0, bytesRead);

                memStream.Write(boundarybytes, 0, boundarybytes.Length);

                fileStream.Close();
            }

            httpWebRequest2.ContentLength = memStream.Length;

            Stream requestStream = httpWebRequest2.GetRequestStream();

            memStream.Position = 0;
            byte[] tempBuffer = new byte[memStream.Length];
            memStream.Read(tempBuffer, 0, tempBuffer.Length);
            memStream.Close();
            requestStream.Write(tempBuffer, 0, tempBuffer.Length);
            requestStream.Close();

            WebResponse webResponse2 = httpWebRequest2.GetResponse();

            Stream stream2 = webResponse2.GetResponseStream();
            StreamReader reader2 = new StreamReader(stream2);

            string ret = reader2.ReadToEnd();

            webResponse2.Close();
            httpWebRequest2 = null;
            webResponse2 = null;

            return ret;
        }
    }
}
