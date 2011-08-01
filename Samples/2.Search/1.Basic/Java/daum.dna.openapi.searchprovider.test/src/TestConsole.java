import responses.*;


public class TestConsole {

		public static void main(String[] args) throws Exception
		{
			BlogData data = OpenApiProvider.requestBlogApi("{발급 받은 키를 입력하세요.}", "apple", 10, 1, "accu", "rss", "");
			
			System.out.print(data);
		}
}
