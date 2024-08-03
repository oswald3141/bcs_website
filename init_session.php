<?php

session_start();

$users = include '../users.php';

if(isset($_REQUEST['login'])){
  $username = $_REQUEST['username'];
  $password = $_REQUEST['password'];

  if( isset($users[$username]) && password_verify($password, $users[$username]['password_hash']) ) {
    $_SESSION['username'] = $username;
    $_SESSION['LOGIN_TIME'] = time();
  }
}

if(isset($_REQUEST['logout'])){
  session_unset();
  session_destroy();
  header("Location: /");
  exit();
}

if (isset($_SESSION['LOGIN_TIME']) && (time() - $_SESSION['LOGIN_TIME'] > 600)) {
  session_unset();
  session_destroy();
  session_start();
}  

if (!empty($_SESSION['username'])) {
  $logged_in = true;
  $username = $_SESSION['username'];
  $user_data = $users[$username];
  $srvs = include '../servers_data.php';
}

?>
