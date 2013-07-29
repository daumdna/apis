<?php
/**
* 마이피플 봇 API 코드 샘플입니다. 
* 
* 마이피플 봇 API를 사용방법에 대해 안내합니다. 
* 알림콜백을 받은 뒤 action값에 따라 처리하는 방식입니다. 
*
* PHP version 5.4.7
*
* @category   Mypopple Bot API
* @author     Daum DNA Lab (http://dna.daum.net)
* @copyright  Daum DNA Lab
* @link       http://dna.daum.net/apis/mypeople
* 
*/

$API_URL_PREFIX = "https://apis.daum.net";
$MYPEOPLE_BOT_APIKEY = "[API KEY를 입력하세요]";
$API_URL_POSTFIX = "&apikey=" .$MYPEOPLE_BOT_APIKEY; 

switch($_POST['action']) {
	case "addBuddy":
		greetingMessageToBuddy();	//봇을 친구로 등록한 사용자의 이름을 가져와 환영 메시지를 보냅니다.
		break;
	case "sendFromMessage":		
		echoMessageToBuddy();		//말을 그대로 따라합니다.
		break;
	case "createGroup":
		groupCreatedMessage();		//그룹대화방이 생성되었을때 그룹대화를 만든사람과 대화에 참여한 친구들의 이름을 출력합니다.
		break;
	case "inviteToGroup":		
		groupGreetingMeesage();		//그룹대화방에 친구가 새로 추가될경우 누가 누구를 초대했는지 출력합니다.
		break;
	case "exitFromGroup":	
		groupExitAlertMessage();	//그룹대화방에서 친구가 나갔을 경우 정보를 출력합니다.
		break;
	case "sendFromGroup":		
		filterGroupMessage();		//그룹 대화방에서 특정 메시지가 왔을때 반응합니다.
		break;
}

function greetingMessageToBuddy()
{
	$buddyId = $_POST['buddyId'];		//봇을 친구추가한 친구ID
	$msg = getBuddyName($buddyId). "님 안녕하세요";

	sendMessage("buddy", $buddyId, $msg);
}

function echoMessageToBuddy()
{
	$buddyId = $_POST['buddyId'];		//메시지를 보낸 친구ID
	$msg =  $_POST['content'];			//메시지 내용
	sendMessage("buddy", $buddyId, $msg);
}

function groupCreatedMessage()
{
	$buddyId = $_POST['buddyId'];		//그룹 대화를 만든 친구 ID
	$content =  $_POST['content'];		//그룹 대화방 친구 목록(json형태)
	$groupId = $_POST['groupId'];		//그룹ID

	$buddys = json_decode($content, true);	
	$buddysName = "";
	foreach($buddys as  $key => $value)
	{
		$buddysName .= " " .getBuddyName($buddys[$key][buddyId]);		
	}
	
	//그룹에 생성메시지 보내기
	$msg = getBuddyName($buddyId). "님이 새로운 그룹대화를 만들었습니다. 그룹멤버는 " .$buddysName. " 입니다.";
	sendMessage("group", $groupId, $msg);
}

function groupGreetingMeesage()
{
	$buddyId = $_POST['buddyId'];		//그룹 대화방에 초대한 친구 ID
	$content =  $_POST['content'];		// 그룹 대화방에 초대된 친구 정보
	$groupId = $_POST['groupId'];		//그룹ID
	
	$buddys = json_decode($content, true);	
	$buddysName = "";
	foreach($buddys as  $key => $value)
	{
		$buddysName .= " " .getBuddyName($buddys[$key][buddyId]);		
	}
		
	//그룹에 환영 메시지 보내기	
	$msg = getBuddyName($buddyId). "님께서 " .$buddysName. "님을 초대하였습니다.";
	sendMessage("group", $groupId, $msg);
}

function groupExitAlertMessage()
{
	$buddyId = $_POST['buddyId'];		//그룹 대화방을 나간 친구 ID
	$groupId = $_POST['groupId'];		//그룹 대화방ID

	//그룹에 퇴장알림 메시지 보내기
	$msg = "슬프게도..." .getBuddyName($buddyId). "님께서 우리를 떠나갔어요.";
	sendMessage("group", $groupId, $msg);
}
function filterGroupMessage()
{
	$groupId = $_POST['groupId'];	//그룹 대화방ID
	$buddyId = $_POST['buddyId'];	//그룹 대화방에서 메시지를 보낸 친구ID
	$content = $_POST['content'];	//메시지 내용

	// "마이피플"이라는 단어가 포함된 메시지가 나오면 반응
	if (strpos($content, '마이피플') !== false)
	{	
		$msg = getBuddyName($buddyId). "님, 역시 마이피플이 짱이죠?";
		sendMessage("group", $groupId, $msg);
	}
	
	//퇴장처리
	if (strcmp($content, '퇴장') == 0 || strcmp($content, 'exit') == 0)
	{
		exitGroup($groupId);	//그룹대화방 퇴장
	}
}
function exitGroup($groupId)
{
	global $API_URL_PREFIX, $API_URL_POSTFIX;
	
	$url =  $API_URL_PREFIX."/mypeople/group/exit.xml?groupId=" .$groupId .$API_URL_POSTFIX;
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt ($ch, CURLOPT_SSL_VERIFYPEER, 0);
	$result = curl_exec($ch);
	curl_close($ch);
}

function sendMessage($target, $targetId, $msg)
{
	global $API_URL_PREFIX, $API_URL_POSTFIX, $MYPEOPLE_BOT_APIKEY;
	
	//메시지 전송 url 지정
	$url =  $API_URL_PREFIX."/mypeople/" .$target. "/send.xml?apikey=" .$MYPEOPLE_BOT_APIKEY;
	
	//CR처리. \n 이 있을경우 에러남
	$msg = urlencode(str_replace(array("\n",'\n'), "\r", $msg));		
	
	//파라미터 설정
	$postData = array();
	$postData[$target."Id"] = $targetId;
	$postData['content'] = $msg;		
	$postVars = http_build_query($postData);
	
	//cURL을 이용한 POST전송
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_POST, 1);
	curl_setopt($ch, CURLOPT_POSTFIELDS, $postVars);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt ($ch, CURLOPT_SSL_VERIFYPEER, 0);
	$result = curl_exec($ch);
	curl_close($ch);
	
	//결과 출력
	echo "sendMessage";
	var_dump($result);
}

function getBuddyName($buddyId)
{
	global $API_URL_PREFIX, $API_URL_POSTFIX;	
	//프로필 정보보기 url 지정
	$url = $API_URL_PREFIX."/mypeople/profile/buddy.xml?buddyId=" .$buddyId .$API_URL_POSTFIX;

	//cURL을 통한 http요청
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt ($ch, CURLOPT_SSL_VERIFYPEER, 0);
	$result = curl_exec($ch);
	curl_close($ch);
	
	//결과 출력
	echo "getBuddyName";
	var_dump($result);
			
	//결과 파싱 및 리턴 
	$xml = simplexml_load_string($result);
	if ($xml->code == 200) {
		return $xml->buddys->name;
	} else {
		return null;		//오류
	}
}

?>

