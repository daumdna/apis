<html>
<head><title>마이피플 봇 API 예제</title></head>
<body>

<h2>마이피플 봇 API 예제</h2>

<div>
<h3>1:1 대화 메시지 보내기</h3>
<form method='post' action='callback.php'>
<input type='hidden' name='action' value='sendFromMessage'></input>
apikey : <input type='text' name='apikey' value='[API KEY를 입력하세요]' /><br />
buddyId : <input type='text' name='buddyId' value='[buudyId를 입력하세요]' /><br />
content : <input type='text' name='content' value='hello' /><br /> 
<input type='submit' value='메시지 전송 실행'/>
</form>
</div>
<hr />
<div>	
<h3>1대1 대화 파일 보내기</h3>
jpg, gif, png만 가능(그룹대화에 전송할 경우 buudyId대신 groupId사용)
<form method="post" enctype="multipart/form-data" action='sendFile.php'>
<input type='hidden' name='action' value='sendFile' />
apikey : <input type='text' name='apikey' value='[API KEY를 입력하세요]' /><br />
buddyId : <input type='text' name='buddyId' value='[buudyId를 입력하세요]' /><br />
file : <input type='file' name='upload' />
<input type='hidden' name='content' value='attach' /><br /> 
<input type='submit' value='파일 전송 실행'/>
</form>	
</div>
<hr />
<div>	
<h3>파일 다운로드</h3>
파일 저장경로는 "서버경로/download" 폴더 입니다
<form method='post' action='download.php'>
<input type='hidden' name='action' value='download'></input>
apikey : <input type='text' name='apikey' value='[API KEY를 입력하세요]' /><br />
fileId : <input type='text' name='fileId' value='myp_pci:51A441100306ED0049' />
<input type='submit' value='파일 다운로드 실행'/>
</form>	
</div>


</body>
</html>