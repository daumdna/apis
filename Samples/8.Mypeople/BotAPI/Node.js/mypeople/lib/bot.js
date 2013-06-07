var req = require('request'),
	fs = require('fs');

(function () {
	'use strict';

	var apiUrl = Array();

	var Bot = module.exports = function (options) {

		if( options!==null && options.apiKey!=="MYPEOPLE_APIKEY" ){
			this.apiHost = options.apiHost;
			this.apiKey = options.apiKey;
			console.log('MyPeople BOT: ', this.apiHost, ',', this.apiKey);
		}else{
			console.log('MyPeople BOT: apiKey를 설정해주세요.')
		}

		apiUrl = {
			buddyProfile: this.apiHost + "/mypeople/profile/buddy.json?apikey=" + this.apiKey,
			sendBuddy: this.apiHost + "/mypeople/buddy/send.json?apikey=" + this.apiKey,
			sendGroup: this.apiHost + "/mypeople/group/send.json?apikey=" + this.apiKey,
			members: this.apiHost + "/mypeople/group/members.json?apikey=" + this.apiKey,
			exitGroup: this.apiHost + "/mypeople/group/exit.json?apikey=" + this.apiKey,
			downloadFile: this.apiHost + "/mypeople/file/download.json?apikey=" + this.apiKey
		}

	};

	Bot.prototype = {

		/**
		* 1:1 대화 메시지 보내기
		*      http://dna.daum.net/apis/mypeople/ref#send1on1message
		*/
		sendMessageToBuddy: function (buddyId, content, attach, callback) {
			if(attach != null) {

				req.post({
					url: apiUrl.sendBuddy,
					headers: {
						'content-type': 'multipart/form-data'
					},
					method: 'POST',
					multipart: [{
						'Content-Disposition': 'form-data; name="attach"; filename="image.jpg"',
						'Content-Type': 'image/jpg',
						body: fs.readFileSync("mypeople/bot_data/" + attach + ".jpg")
					}, {
						'Content-Disposition': 'form-data; name="buddyId"',
						body: buddyId
					}]
				}, this.createResponseHandler(callback));

			} else {

				req.get({
					uri: apiUrl.sendBuddy + "&buddyId=" + buddyId + "&content=" + encodeURIComponent(content)
				}, this.createResponseHandler(callback));

			}
		},

		/**
		* 친구 프로필 정보 보기
		*      http://dna.daum.net/apis/mypeople/ref#getfriendsinfo
		*/
		buddyProfile: function (buddyId, callback) {
			req.get({
				uri: apiUrl.buddyProfile + "&buddyId=" + buddyId
			}, this.createProfileResponseHandler(callback));
		},

		/**
		* 그룹 대화방 친구 목록 보기
		*      http://dna.daum.net/apis/mypeople/ref#groupuserlist
		*/
		getMembers: function (groupId, callback) {
			req.get({
				uri: apiUrl.members + "&groupId=" + groupId
			}, this.createProfileResponseHandler(callback));
		},

		/**
		* 그룹 대화방에 메시지 보내기
		*      http://dna.daum.net/apis/mypeople/ref#sendgroupmessage
		*/
		sendMessageToGroup: function (groupId, content, attach, callback) {

			if(attach != null) {

				req.post({
					url: apiUrl.sendGroup,
					headers: {
						'content-type': 'multipart/form-data'
					},
					method: 'POST',
					multipart: [{
						'Content-Disposition': 'form-data; name="attach"; filename="image.jpg"',
						'Content-Type': 'image/jpg',
						body: fs.readFileSync("mypeople/bot_data/" + attach + ".jpg")
					}, {
						'Content-Disposition': 'form-data; name="groupId"',
						body: groupId
					}]
				}, this.createResponseHandler(callback));

			} else {

				req.get({
					uri: apiUrl.sendGroup + "&groupId=" + groupId + "&content=" + encodeURIComponent(content)
				}, this.createResponseHandler(callback));

			}
		},

		/**
		* 그룹 대화방 나가기
		*      http://dna.daum.net/apis/mypeople/ref#leavegroup
		*/
		exitFromGroup: function (groupId, callback) {

			req.get({
				uri: apiUrl.exitGroup + "&groupId=" + groupId
			}, this.createResponseHandler(callback));

		},

		/**
		 * 파일 및 사진 받기
		 *      http://dna.daum.net/apis/mypeople/ref#filedownload      
		 */
		downloadFile: function (fileId, fileName) {

			req.get({
				uri: apiUrl.downloadFile + "&fileId=" + fileId,
			}).pipe(fs.createWriteStream('mypeople/bot_data/download/' + fileName + '.jpg'));
			
		},


		createResponseHandler: function (callback) {
			return function (error, resp, data) {

				if (error) {
					callback(error, null);
				} else {
					var result;
					try {
						result = JSON.parse(data);
					} catch (e) {
						callback("Error : JSON Parsing", e);
					}

					if (parseInt(result.code, 10) === 200) {
						callback(null, result);
					} else {
						callback("Error : Request\n" + resp.request.uri.href + "\n" + data, null);
					}
				}

			};

		},

		createProfileResponseHandler: function (callback) {
			return function (error, resp, data) {

				if (error) {
					callback(error, null);
				} else {
					var result;

					try {
						result = JSON.parse(data);
					} catch (e) {
						callback("Error : JSON Parsing", e);
					}

					if (parseInt(result.code, 10) === 200) {
						if(result.buddys[0] === undefined){
							callback("Error : Profile is undefined", null);
						}else{
							callback(null, result);
						}
					} else {
						callback("Error : Request\n" + resp.request.uri.href + "\n" + data, null);
					}
				}

			};

		}

	};

})();
