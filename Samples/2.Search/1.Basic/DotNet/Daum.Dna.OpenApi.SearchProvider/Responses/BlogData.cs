using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Daum.Dna.OpenApi.SearchProvider.Responses
{
    public class BlogData
    {
        public string Title { get; set; }
        public string Link { get; set; }
        public string Description { get; set; }
        public string LastBuildDate { get; set; }
        public int TotalCount { get; set; }
        public int PageCount { get; set; }
        public int Result { get; set; }
        public List<BlogItemData> Items { get; private set; }

        public BlogData()
        {
            Items = new List<BlogItemData>();
        }

        public override string ToString()
        {
            String outStr = "";
            outStr += "title" + ":" + Title + "\n";
            outStr += "link" + ":" + Link + "\n";
            outStr += "description" + ":" + Description + "\n";
            outStr += "lastBuildDate" + ":" + LastBuildDate + "\n";
            outStr += "totalCount" + ":" + TotalCount + "\n";
            outStr += "pageCount" + ":" + PageCount + "\n";
            outStr += "result" + ":" + Result + "\n";
            outStr += "itemsCount" + ":" + Items.Count + "\n\n";

            for (int i = 0; i < Items.Count; i++)
            {
                outStr += "item(" + i + ")\n";
                outStr += "item(" + i + ") title:" + Items[i].Title + "\n";
                outStr += "item(" + i + ") link:" + Items[i].Link + "\n";
                outStr += "item(" + i + ") description:" + Items[i].Description + "\n";
                outStr += "item(" + i + ") comment:" + Items[i].Comment + "\n";
                outStr += "item(" + i + ") author:" + Items[i].Author + "\n";
                outStr += "item(" + i + ") pubDate:" + Items[i].PubDate + "\n\n";
            }

            return outStr;
        }
    }
}
