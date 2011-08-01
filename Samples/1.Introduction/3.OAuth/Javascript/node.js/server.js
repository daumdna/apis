var express = require('express');
var sys = require('sys');
var oauth = require('oauth');

var app = express.createServer();

var ConsumerKey = "발급받으신 ConsumerKey를 입력하세요.";
var ConsumerSecret = "발급받으신 ConsumerSecret를 입력하세요.";
var CallbackUrl = "등록하신 CallbackUrl을 입력하세요.";

ConsumerKey = "524c4867-7702-4d1a-96f3-4ec70a83e77c";
ConsumerSecret = "Ei7iDTM5IXaFEFh4Ku1XjAPe8vojKk6sP15Mq_KgRvkRwQcFV_GK4g00";
CallbackUrl = "http://mademin.com:8002/callback";

var RequestTokenUrl = "https://apis.daum.net/oauth/requestToken";
var AuthorizeUrl = "https://apis.daum.net/oauth/authorize";
var AccessTokenUrl = "https://apis.daum.net/oauth/accessToken";
var ResourceUrl = "https://apis.daum.net/calendar/event/index.json";

//ConsumerKey = "ntXKmszjueD2jfaDytv07A";
//CunsoumerSecret = "0j1Bs2yeeTTjITTB6OJpnvBMqptYsm0z054IEsIJ0I";
//RequestTokenUrl = "https://api.twitter.com/oauth/request_token";
//AuthorizeUrl = "https://api.twitter.com/oauth/authorize";
//AccessTokenUrl = "https://api.twitter.com/oauth/access_token";
//ResourceUrl = "";

app.configure('development', function(){
        app.use(express.errorHandler({ dumpExceptions: true, showStack: true }));
        app.use(express.logger());
        app.use(express.cookieParser());
        app.use(express.bodyParser());
        app.use(express.session({ secret : 'test!@#'}));
        });

app.dynamicHelpers({
session: function(req, res){
return req.session;
}
});

function consumer() {
    return new oauth.OAuth(
            RequestTokenUrl, AccessTokenUrl, 
            ConsumerKey, ConsumerSecret, "1.0", CallbackUrl, "HMAC-SHA1");   
}
//RequestToken & Authorize
app.get('/', function(req, res){
        consumer().getOAuthRequestToken(function(error, oauthToken, oauthTokenSecret, results){
            if (error) {
            res.end("Error getting OAuth request token : " + sys.inspect(error), 500);
            } else {  
            req.session.oauthRequestToken = oauthToken;
            req.session.oauthRequestTokenSecret = oauthTokenSecret;
            res.redirect(AuthorizeUrl+"?oauth_token="+req.session.oauthRequestToken);      
            }
            });
        });
//callback(verify) & RequestAccessToken
app.get('/callback', function(req, res){
        consumer().getOAuthAccessToken(req.session.oauthRequestToken, req.session.oauthRequestTokenSecret, req.query.oauth_verifier, function(error, oauthAccessToken, oauthAccessTokenSecret, results) {
            if (error) {
                res.end("Error getting OAuth access token : " + sys.inspect(error) + "["+oauthAccessToken+"]"+ "["+oauthAccessTokenSecret+"]"+ "["+sys.inspect(results)+"]", 500);
            } else {
                req.session.oauthAccessToken = oauthAccessToken;
                req.session.oauthAccessTokenSecret = oauthAccessTokenSecret;
                res.redirect('/resource');
                }
            });
   });
//AccessProtectedResource
app.get('/resource',function(req,res){
    requestParameters = {'start_at':'2011-01-01','end_at':'2011-12-31'};
    consumer().post(ResourceUrl, req.session.oauthAccessToken, req.session.oauthAccessTokenSecret, requestParameters, null, function (error, data, response) {
        if (error) {
            res.end("Error getting Daum callender event : " + sys.inspect(error), 500);
        } else {
            //Convert string to json
            var jsonData = eval('('+data+')');
            var tempHTML = '';
            
            res.writeHead(200, {'Content-Type': 'text/html;charset=utf-8'});
            if (jsonData.code == '500'){
                res.end(data); 
            } else {
                for (var i in jsonData){
                    tempHTML += "일정 제목 ->" + jsonData[i].title + "<br>";
                    tempHTML += "일정 내용 ->" + jsonData[i].description + "<br>";
                    tempHTML += "-----------------------<br>";
                }
                res.end(tempHTML);
            }
        }
    });
});

app.listen(parseInt(process.env.PORT || 8002));
