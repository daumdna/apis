// 1. URL 및 Consumer 정보 설정
var config = {
	requestTokenUrl: "https://apis.daum.net/oauth/requestToken",
	authorizeUrl: "https://apis.daum.net/oauth/authorize",
	accessTokenUrl: "https://apis.daum.net/oauth/accessToken",
	consumerKey: "[Consumer 등록 후 각자 입력하세요]",
	consumerSecret: "[Consumer 등록 후 각자 입력하세요]",
	callbackUrl: "oob",
	apiUrl: "https://apis.daum.net"
}

// 외부 모듈에서 사용할 수 있도록 export
exports.config = config;
