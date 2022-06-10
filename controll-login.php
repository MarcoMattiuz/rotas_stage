<?php
session_start();
$dbname = 'accountRobot';
$dbuser = 'root';
$dbpass = 'rotas';
$dbhost = 'localhost';
echo "1";
$username = $_POST['username']; 
$password = $_POST['password'];
echo "$username"," ",$password;
if($username == "admin"){
    if($password=="rotas88"){
        $_SESSION["login"] = true;
        header("location:index.php");
        exit();
    }
}
header("location:login.php");


// $connect = mysqli_connect($dbhost, $dbuser, $dbpass,$dbname);
// if(mysqli_connect_errno()){
//     echo "1. Unable to connect to '$dbhost'";
// }
// echo "2";
// $username = $_SESSION['username'];
// $password = $_SESSION['password'];
// echo $username;
// $query = "SELECT * FROM accounts WHERE username = '$username'";  

// $result = mysqli_query($connect, $query)or die("2. query failed");;  
// if(mysqli_num_rows($result) > 0){
//     exit();
// } 
// echo "3";
?>