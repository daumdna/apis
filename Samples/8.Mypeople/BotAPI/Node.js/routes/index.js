exports.index = function(req, res){
 	res.render('index', { title: '마이피플 봇 예제' });
};

exports.test = function(req, res){
 	res.render('test', { 
 		title: '마이피플 봇 API 테스트 폼',
 		apikey: 'MYPEOPLE_APIKEY',
 		groupId: 'GROUPID',
 		buddyId: 'BUDDYID' 		
 	 });
};
