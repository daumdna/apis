var fs = require('fs');
var Client = require('mypeople').Client;
var client = new Client("MYPEOPLE_KEY", {server: 'https://apis.daum.net'});

exports.buddyTest = function(buddyId, content) {

	// 친구 추가 메세지 테스트
	this.addBuddy(buddyId);

	// 메세지 전송 테스트
	this.sendFromMessage(buddyId, content);

	// 이미지 전송 테스트
	this.sendFromImage(buddyId);

	// 이미지 다운로드 테스트(bot_data/download)
	this.profileDownload(buddyId);

};

exports.addBuddy = function(buddyId) {

	client.getFriendInfo(buddyId, function(error, buddys) {
		if(!error){
			var reply = buddys[0].name + '님 반갑습니다.';
			client.sendMessage(buddyId, reply, function(error, data) {
				if(!error){
					console.log(data);
				}else{
					console.log(error);
				}
			});			
		}else{
 			console.log(error);
 		} 
	});

};

exports.sendFromMessage = function(buddyId, content) {

	client.getFriendInfo(buddyId, function(error, buddys) {
		if(!error){

			var reply = buddys[0].name + ': ' + content;
			client.sendMessage(buddyId, reply, function(error, data) {
				if(!error){
					console.log(data);
				}else{
					console.log(error);
				}
			});	

		}else{
 			console.log(error);
 		} 
	});

};

exports.sendFromImage = function(buddyId) {

	client.sendMessage(buddyId, fs.createReadStream('mypeople/bot_data/image_cat.jpg'), function(error, data) {
		if(!error){
			console.log(data);
		}else{
			console.log(error);
		}
	});

};

exports.profileDownload = function(buddyId) {

	client.getFriendInfo(buddyId, function(error, buddys) {
		if(!error){

			client.download(buddys[0].photoId, function(error, data) {
				if(!error){
					console.log(data);
				}else{
					console.log(error);
				}
			}).pipe(fs.createWriteStream('mypeople/bot_data/download/' + buddys[0].buddyId + '.jpg'));

		}else{
			console.log(error);
		}	
	});

};

exports.groupTest = function(groupId, buddyId, content, inviteTest) {

	// 그룹 메세지 테스트
	this.sendFromGroup(groupId, content);

	// 그룹 맴버 목록 테스트
	this.getMembers(groupId);

	// getMebers로 출력된 buddyId를 입력하여 테스트
	var testUser="BU_iOYEwdlbrLsZqM14QZaXVw00";

	// 방생성 이벤트
	this.createGroup(groupId, testUser);
	
	// 초대 이벤트
	this.inviteToGroup(groupId, testUser, inviteTest);			

	// 퇴장 메세지 테스트
	this.exitFromGroup(groupId, testUser);

};

exports.getMembers = function(groupId) {

	client.getGroupMembers(groupId, function(error, buddys) {

		if(!error){
			// data.buddys
			// [ { buddyId: 'BU_vy8zKcwnpj5UPJ6HXnSF9w00',
			//     photoId: 'myp_pub:51AD2346061F2F000E',
			//     name: '똑똑박사' },
			//   { buddyId: 'BU_iOYEwdlbrLsZqM14QZaXVw00',
			//     photoId: 'myp_pub:515A862A032BBB000D',
			//     name: '한승호' },
			//   { buddyId: 'BU_1M9qHDITjlU0',
			//     photoId: 'myp_pub:4FE5829B04234E0031',
			//     name: '봇구' } ]
			var members = buddys.map(function (user) {
				return user.name + ' ( ' + user.buddyId + ' )';
			}).join('\n');

			client.sendGroupMessage(groupId, members, function(error, data) {
				if(!error){
					console.log(data);
				}else{
					console.log(error);
				}
			});

		}else{
			console.log(error);
		}
	});

};

exports.sendFromGroup = function(groupId, buddyId, content, attache) {

	client.getFriendInfo(buddyId, function(error, buddys) {
		if(!error){

			var reply = buddys[0].name + ': ' + content;
			client.sendGroupMessage(groupId, reply, function(error, data) {
				if(!error){
					console.log(data);
				}else{
					console.log(error);
				}
			});

		}else{
 			console.log(error);
 		} 
	});

};

exports.createGroup = function(groupId, buddyId) {

	client.getFriendInfo(buddyId, function(error, buddys) {
		if(!error){

			var reply = buddys[0].name + '님 반갑습니다.';
			client.sendGroupMessage(groupId, reply, function(error, data) {
				if(!error){
					console.log(data);
				}else{
					console.log(error);
				}
			});

		}else{
			console.log(error);
		}
	});

};

exports.inviteToGroup = function(groupId, buddyId, content) {

	// content
	// [{"buddyId":"BU_1M9qHDITjlU0","isBot":"N","name":"초대남","photoId":"myp_pub:4FE5829B04234E0031"}]
	try {
		var user = JSON.parse(content);
	} catch (e) {
		console.log("Error : invite content JSON Parsing", e);
	}

	var members = user.map(function (user) {
		return user.name;
	}).join('님, ');


	client.getFriendInfo(buddyId, function(error, buddys) {
		if(!error){


			var reply = buddys[0].name + '님이 ' + members + '님을 초대하였습니다.';
			client.sendGroupMessage(groupId, reply, function(error, data) {
				if(!error){
					console.log(data);
				}else{
					console.log(error);
				}
			});

		}else{
			console.log(error);
		}
	});

};

exports.exitFromGroup = function(groupId, buddyId) {

	client.getFriendInfo(buddyId, function(error, buddys) {
		if(!error){

			var reply = buddys[0].name + '님 잘가요~ ㅠ';
			client.sendGroupMessage(groupId, reply, function(error, data) {
				if(!error){
					console.log(data);
				}else{
					console.log(error);
				}
			});

		}else{
			console.log(error);
		}
	});

};

exports.exitBot = function(groupId, buddyId) {

	client.exitGroup(groupId, function(error, data) {
		if(!error){
			console.log(data);
		}else{
			console.log(error);
		}
	});

};
