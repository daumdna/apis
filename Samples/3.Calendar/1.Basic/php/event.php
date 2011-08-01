<?php
require "config.php";
require "lib.php";
session_start();

if(!$_SESSION['access_token'] ) {
	header("Location: ./index.php");
} else {
    $oauth->setToken($_SESSION['access_token'], $_SESSION['access_token_secret']);
}

$today = date("Y-m-d", time());
?>
<!doctype html>
<html>
<head>
<script>
function checkSubmit(f) {

	if(!start_at || !end_at)
		return false;
	else {
		f.submit();
	}

}
</script>
<title></title>
</head>
<body>
<?php include "head.php"; ?>
<h1>일정 추가</h1>

<form action="./addEvent.php" method="POST" onsubmit="return checkSubmit(this)" name="frmEvent">
<label>카테고리</label>
<select name="category_id">
<?
	$categories = getCategories(); // lib.php에 정의
	$categoryMap = array();

	foreach($categories as $category) {
		// 카테고리ID를 key로 해서 상세정보를 얻을 수 있는 category Map 구성
		$categoryMap[$category->id] = $category;
		echo "<option value=\"".$category->id."\">";
		echo $category->name;
		echo "</option>";
	}

?>
</select>
<label>제목</label>
<input type="text" name="title"/>
<label>시작일</label>
<input type="date" name="start_at" value="<?=$today?>"/>
<label>종료일</label>
<input type="date" name="end_at" value="<?=$today?>"/>
<button type="submit">추가</button>
</form>
<hr/>
<h1>일정 조회/수정/삭제</h1>
<div class="event">
<?php
	$events = getEvents();  // lib.php에 정의

    $msg = "<ul>";
    foreach($events as $event) {
		// 해당 일정의 카테고리 상세 정보를 가져옴
		$category = $categoryMap[$event->category_id];
		$msg.= "<li>";
		$msg.= "<span style=\"background-color:".$category->color."; color:white;\">".$category->name."</span>";
		$msg.= " [".$event->title."] ";
		$msg.= date("Y-m-d", $event->start_at/1000)." ~ ";
		$msg.= date("Y-m-d", $event->end_at/1000).": ";
		$msg.= " <a href=\"./editEvent.php?id=".$event->id."\">수정</a> ";
		$msg.= "<a href=\"./deleteEvent.php?id=".$event->id."\" onclick=\"return confirm('정말 삭제하시겠습니까?')\">삭제</a> ";
		$msg.= "</li>";	
    }
    $msg.="</ul>";

	echo $msg;
?>
</div>
<hr/>
</body>
</html>
