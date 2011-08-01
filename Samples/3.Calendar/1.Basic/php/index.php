<?php
require "config.php";
require "lib.php";

session_start();

// access_token이 발급된 상태가 아니라면, OAuth 인증 절차 시작
if(!$_SESSION['access_token'] ) {

	try {
	    // Request Token 요청
	    $request_token_info = $oauth->getRequestToken($request_token_url, $callback_url);
	    
	    // 얻어온 Request Token을 이후 Access Token과 교환하기 위해 session에 저장.
	    $_SESSION["request_token_secret"] = $request_token_info["oauth_token_secret"];

	    // 사용자 인증 URL로 redirect
	    header('Location: '.$authorize_url.'?oauth_token='.$request_token_info['oauth_token']);
		exit;
	} catch(OAuthException $E) {
		print_r($E);
		exit;
	}
} else {
// Access Token이 이미 발급 되어 있는 상태면, 토큰 지정
    $oauth->setToken($_SESSION['access_token'],$_SESSION['access_token_secret']);
}

?>
<!doctype html>
<html>
<head>
<title>캘린더 API 예제</title>
</head>
<body>
<?php	include "head.php"; ?>
<h1>카테고리 추가</h1>

<form action="addCategory.php" method="POST">
<label>카테고리명</label>
<input name="name" type="text" value="사적인 일"/>
<label>색깔</label>
<input name="color" type="color" value="#f49797"/>
<label>설명</table>
<input type="text" name="description" value="개인적인 일입니다."/>
<button type="submit">추가</button>
</form>
<hr/>
<h1>카테고리 조회 및 수정</h1>
<div id="category">
<?php
	$categories = getCategories();

    $msg = "<ul>";
    foreach($categories as $category) {
		$msg.= "<li>";
		$msg.= "<span style=\"background-color:".$category->color."; color:white;\">".$category->name."</span>";
		$msg.= " <a href=\"editCategory.php?category_id=".$category->id."\">수정</a>";
		$msg.= "</li>";
    }
    $msg.="</ul>";

	echo $msg;
?>
</div>
<hr/>
</body>
</html>

