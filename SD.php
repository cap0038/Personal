<html>

	<head>
	
		<link rel="stylesheet" type="text/css" href="SDStyle.css">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		
	
		
	</head>
	
	<body>
		<form method="post" action="" autocomplete="off">
			<div class="box">
				<div class="imgcontainer">
					<img src="avatarLogo.png" alt="Avatar" class="Rheem">
				</div>
				<label for="user"><b>Email Address</b></label><br>
				<input type="text" name="user" class="user" id="user"><br>
				<label for="pass"><b>Password</b></label><br>
				<input type="password" name="pass" class="user" id="pass"><br>
				<input type="checkbox" onclick="passToggle()">Show Password
				
				<button type="button" onclick="" class="btn">Login</button>
				<button type="button" onclick="" class="btn2">Create Account</button>
			</div>
		</form>
		
		<script>
			function passToggle() {
				var x = document.getElementById("pass");
				if (x.type === "password") {
					x.type = "text";
				}
				else {
					x.type = "password";
				}
			}
		</script>
		
	</body>
</html>