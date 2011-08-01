using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Daum.Dna.OpenApi.SearchProvider.Responses;
using System.Net;
using System.IO;
using System.Xml.Linq;

namespace Daum.Dna.OpenApi.SearchProvider
{
    public class OpenApiProvider
    {
        public static BlogData RequestBlogApi(String apiKey, String q, int result, int pageno, String sort, String output, String callback)
        {
            //링크 주소 만들기
            String requestUrl = RequestUrls.BLOG_REQUEST_URL;
            requestUrl += "?apikey=" + apiKey;
            requestUrl += "&q=" + q;
            requestUrl += "&result=" + result;
            requestUrl += "&pageno=" + pageno;
            requestUrl += "&sort=" + sort;
            requestUrl += "&output=" + output;
            requestUrl += "&callback=" + callback;

            WebRequest wr = WebRequest.Create(requestUrl);
            WebResponse wrp = wr.GetResponse();

            XDocument xd = XDocument.Load(wrp.GetResponseStream());
            
            IEnumerable<XElement> xerr = xd.Descendants("apierror");

            if (xerr.Count() > 0)
            {
                String errMsg = "";
                foreach (XElement xes in xerr)
                {
                    errMsg += xes.Name + "-" + xes.Value + "/";
                }

                throw new Exception(errMsg);
            }

            //빈 완료 객체 만들기
            BlogData data = new BlogData();

            XElement xChannel = xd.Element("rss").Element("channel");

            data.Title = xChannel.Element("title").Value;
            data.Description = xChannel.Element("description").Value;
            data.Link = xChannel.Element("link").Value;
            data.LastBuildDate = xChannel.Element("lastBuildDate").Value;
            data.TotalCount = int.Parse(xChannel.Element("totalCount").Value);
            data.PageCount = int.Parse(xChannel.Element("pageCount").Value);
            data.Result = int.Parse(xChannel.Element("result").Value);

            foreach (XElement xe in xChannel.Elements("item"))
            {
                BlogItemData item = new BlogItemData();
                item.Title = xe.Element("title").Value;
                item.Description = xe.Element("description").Value;
                item.Link = xe.Element("link").Value;
                item.Author = xe.Element("author").Value;
                item.Comment = xe.Element("comment").Value;
                item.PubDate = xe.Element("pubDate").Value;
                data.Items.Add(item);
            }

            return data;
        }
    }
}
