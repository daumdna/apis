<?php
require "config.php";
session_start();

if(!$_SESSION['access_token'] ) {
	header("Location: ./index.php");
} else {
	$category_id = $_GET['category_id'] ? $_GET['category_id'] : $_POST['category_id'];
	$name = $_POST['name'];
	$color = $_POST['color'];
	$description = $_POST['description'];

	try {
		// Access Token이 이미 발급 되어 있는 상태면, 토큰 지정
		$oauth->setToken($_SESSION['access_token'],$_SESSION['access_token_secret']);


		if($name || $color || $description ) {
		    // 수정
		    $parameters = array("name" => $name, "color" => $color, "description" => $description);
		    $oauth->fetch($api_url."/calendar/category/update/".$category_id.".json", $parameters, "POST");
		
		    $json = json_decode($oauth->getLastResponse());
		    
		    echo "<a href=\"./index.php\">[".$json->name."](으)로 수정 되었습니다.</a>";
		    exit;
		} else {
		    // $category_id 조회
		    $oauth->fetch($api_url."/calendar/category/show/".$category_id.".json");
	
		    $json = json_decode($oauth->getLastResponse());
		    
		    $name = $json->name;
		    $color = $json->color;
		    $description = $json->description;
		}

	} catch(OAuthException $E) {
		print_r($E);
	}
}
?>
<!doctype html>
<html>
<head>
<title>캘린더 API - 카테고리 수정</title>
</head>
<body>
<form action="<?=$_SERVER["PHP_SELF"]?>" method="POST">
<input name="category_id" type="hidden" value="<?=$category_id?>"/>
<ul>
<li>
<label>카테고리명</label>
<input id="categoryName" name="name" type="text" value="<?=$name?>"/>
</li>
<li>
<label>색깔</label>
<input id="categoryColor" name="color" type="color" value="<?=$color?>"/>
</li>
<li>
<label>설명</table>
<textarea id="categoryDescription" name="description"><?=$description?></textarea>
</li>
</ul>
<button type="submit">수정</button>
</form>
</body>
</html>
