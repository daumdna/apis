<?php
require "config.php";
require "lib.php";
session_start();

if(!$_SESSION['access_token'] ) {
	header("Location: ./index.php");
} else {
	$id = $_GET['id'] ? $_GET['id'] : $_POST['id'];
	$title = $_POST['title'];
	$start_at = $_POST['start_at'];
	$end_at = $_POST['end_at'];

	try {
		// Access Token이 이미 발급 되어 있는 상태면, 토큰 지정
		$oauth->setToken($_SESSION['access_token'],$_SESSION['access_token_secret']);

		if($title || $start_at || $end_at ) {
		    // 수정
		    $parameters = array("category_id" => $category_id, "title" => $title, "start_at" => $start_at, "end_at" => $end_at);
		    $oauth->fetch($api_url."/calendar/event/update/".$id.".json", $parameters, "POST");
		
		    $json = json_decode($oauth->getLastResponse());
		    echo "<a href=\"./event.php\">[".$json->title."]이 수정 되었습니다.</a>";
		    exit;
		} else {
		    // event 조회
		    $oauth->fetch($api_url."/calendar/event/show/".$id.".json");
	
		    $json = json_decode($oauth->getLastResponse());
		    
		    $title = $json->title;
			$category_id = $json->category_id;
		    $start_at = date("Y-m-d", $json->start_at/1000);
		    $end_at = date("Y-m-d", $json->end_at/1000);
		}

	} catch(OAuthException $E) {
		print_r($E);
	}
}
?>
<!doctype html>
<html>
<head>
<title>캘린더 API - 일정 수정</title>
</head>
<body>
<h1>일정수정</h1>
<form action="<?=$_SERVER["PHP_SELF"]?>" method="POST">
<input name="id" type="hidden" value="<?=$id?>"/>
<label>카테고리</label>
<select name="category_id">
<?
	$categories = getCategories();

	foreach($categories as $category) {
		$selected = "".$category->id == $category_id ? "selected" : "";
		echo "<option value=\"".$category->id."\" ".$selected.">";
		echo $category->name;
		echo "</option>";

	}

?>
</select>
<label>제목</label>
<input name="title" type="text" value="<?=$title?>"/>
<label>시작일시</label>
<input name="start_at" type="date" value="<?=$start_at?>"/>
<label>종료일시</label>
<input name="end_at" type="date" value="<?=$end_at?>"/>
<button type="submit">수정</button>
</form>
</body>
</html>
