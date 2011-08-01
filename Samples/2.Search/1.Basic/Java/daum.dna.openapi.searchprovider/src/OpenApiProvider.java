import java.net.*;
import javax.xml.parsers.*;
import org.w3c.dom.Document;
import org.w3c.dom.Node;
import responses.*;

public class OpenApiProvider {
	
	public static BlogData requestBlogApi(String apiKey, String q,int result, int pageno, String sort,String output,String callback) throws Exception 
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
		URL url = new URL(requestUrl);
		
		//API 요청 및 반환
		URLConnection conn = url.openConnection();
		DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
		DocumentBuilder builder = factory.newDocumentBuilder();
		Document doc = builder.parse(conn.getInputStream());
		
		//에러체크
		if(doc.getElementsByTagName("apierror").getLength() > 0)
		{
			Node node = doc.getElementsByTagName("apierror").item(0);
			
			String errMsg = "";
			for (int i=0 ;i< node.getChildNodes().getLength();i++) {
				errMsg += node.getChildNodes().item(i).getNodeName() + "-" + node.getChildNodes().item(i).getTextContent() + "/";
			} 
			throw new Exception(errMsg);
		}
		
		//빈 완료 객체 만들기
		BlogData data = new BlogData();
		
		//channel노드를 객체화 하기
		Node node = doc.getElementsByTagName("channel").item(0);
		for (int i=0 ;i< node.getChildNodes().getLength();i++) {
			Node channelNode = node.getChildNodes().item(i);
			String nodeName = channelNode.getNodeName();
			if ("title".equals(nodeName))
				data.setTitle(channelNode.getTextContent());
			else if ("description".equals(nodeName))
				data.setDescription(channelNode.getTextContent());
			else if ("link".equals(nodeName))
				data.setLink(channelNode.getTextContent());
			else if ("lastBuildDate".equals(nodeName))
				data.setLastBuildDate(channelNode.getTextContent());
			else if ("totalCount".equals(nodeName))
				data.setTotalCount(Integer.parseInt(channelNode.getTextContent()));
			else if ("pageCount".equals(nodeName))
				data.setPageCount(Integer.parseInt(channelNode.getTextContent()));
			else if ("result".equals(nodeName))
				data.setResult(Integer.parseInt(channelNode.getTextContent()));
			else if ("item".equals(nodeName)) 
			{
				//item노드를 객체화 하기
				BlogItemData blogItem = new BlogItemData(); 
				for (int j=0 ;j< channelNode.getChildNodes().getLength();j++) {
					Node itemNode = channelNode.getChildNodes().item(j);
					if("title".equals(itemNode.getNodeName()))					
						blogItem.setTitle(itemNode.getTextContent());
					else if("description".equals(itemNode.getNodeName()))
						blogItem.setDescription(itemNode.getTextContent());
					else if("link".equals(itemNode.getNodeName()))
						blogItem.setLink(itemNode.getTextContent());
					else if("author".equals(itemNode.getNodeName()))
						blogItem.setAuthor(itemNode.getTextContent());
					else if("comment".equals(itemNode.getNodeName()))
						blogItem.setComment(itemNode.getTextContent());
					else if("pubDate".equals(itemNode.getNodeName()))
						blogItem.setPubDate(itemNode.getTextContent());
				}
				data.getItems().add(blogItem);
			}
		}
		return data;
	}
}
