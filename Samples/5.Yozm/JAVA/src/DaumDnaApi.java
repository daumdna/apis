import org.scribe.builder.api.*;
import org.scribe.model.*;

public class DaumDnaApi extends DefaultApi10a 
{
  private static final String AUTHORIZE_URL = "https://apis.daum.net/oauth/authorize";
  private static final String REQUEST_TOKEN_RESOURCE = "apis.daum.net/oauth/requestToken";
  private static final String ACCESS_TOKEN_RESOURCE = "apis.daum.net/oauth/accessToken";
  
  @Override
  public String getAccessTokenEndpoint()
  {
    return "https://" + ACCESS_TOKEN_RESOURCE;
  }

  @Override
  public String getRequestTokenEndpoint()
  {
    return "https://" + REQUEST_TOKEN_RESOURCE;
  }

  @Override
  public String getAuthorizationUrl(Token requestToken)
  {
    return String.format(AUTHORIZE_URL, requestToken.getToken());
  }

  public static class SSL extends DaumDnaApi
  {
    @Override
    public String getAccessTokenEndpoint()
    {
      return "https://" + ACCESS_TOKEN_RESOURCE;
    }

    @Override
    public String getRequestTokenEndpoint()
    {
      return "https://" + REQUEST_TOKEN_RESOURCE;
    }
  }
}
