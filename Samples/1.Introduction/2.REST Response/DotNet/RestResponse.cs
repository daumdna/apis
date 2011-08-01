using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Daum.Dna.OpenApi.Example.Introduction
{
    class RestResponse
    {
        static void Main(string[] args)
        {
            //링크 주소 만들기 - love를 검색하고 검색 된 20개의 아이템을 xml로 받고 1페이지를 싶을때
            String requestUrl = "http://apis.daum.net/search/blog";
            requestUrl += "?apikey=" + "DAUM_SEARCH_DEMO_APIKEY"; //발급된 키
            requestUrl += "&q=" + "love"; //검색어
            requestUrl += "&result=" + "20"; //출력될 결과수w
            requestUrl += "&pageno=" + "1"; //페이지 번호
            requestUrl += "&output=" + "xml";

            //최종 url = http://apis.daum.net/search/blog?apikey=DAUM_SEARCH_DEMO_APIKEY&q=love&&result=20&&pageno=1&output=xml

            //웹요청 객체를 만든다.
            System.Net.WebRequest wr = System.Net.WebRequest.Create(requestUrl);

            //웹요청을 실행하고 그에 대한 응답객체를 만든다.
            System.Net.WebResponse wrp = wr.GetResponse();

            //응답은 XML이므로 XML문서로 구조화한다.
            System.Xml.Linq.XDocument xd = System.Xml.Linq.XDocument.Load(wrp.GetResponseStream());

            //출력된 Title을 모두 보여준다.
            foreach (System.Xml.Linq.XElement xEle in xd.Root.Elements("item"))
            {
                System.Console.WriteLine(xEle.Element("title").Value);
            }
        }
    }
}
