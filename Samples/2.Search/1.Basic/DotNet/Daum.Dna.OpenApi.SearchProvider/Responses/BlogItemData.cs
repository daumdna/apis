using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Daum.Dna.OpenApi.SearchProvider.Responses
{
    public class BlogItemData
    {
        public string Title { get; set; }
        public string Link { get; set; }
        public string Description { get; set; }
        public string Comment { get; set; }
        public string Author { get; set; }
        public string PubDate { get; set; }
    }
}
