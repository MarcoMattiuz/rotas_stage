<?php 
    session_start();


?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="web/src_CSS/login.css" />
    <title>login</title>
</head>
<body>
    <div class="outer-container">
        <div class="description">
            <h1>WELCOME BACK!</h1>
            <p>
                Log-in to see and command this rover moving. <br> 
                Our mission is to imagine and create exceptional 
                robots that enrich people's lives. Discover Spot,
                 Stretch, and our other robots.<br><br>
                
                Rotas.
            </p>
        </div>
        <div class="wrapper">
            <div class="heading">
                Sign-in
            </div>
            <form action="index.php">
                <div class="column-fields">
                    <div class="wrap">
                        <label>Username</label>
                        <input type="text" name="username" class="input-field" placeholder="username">
                    </div>
                    <div class="wrap">
                        <label>Password</label>
                        <input type="password" name="password" class="input-field" placeholder="password">
                    </div>
                </div>
                <input type="button" name="submit" class="input-submit" value="Login" disabled>
            </form>              
        </div>
       
     
    </div>


</body>
</html>