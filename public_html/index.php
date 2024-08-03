<?php include '../init_session.php';?>

<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css">

    <title>BCServers</title>
  </head>
  <body>
    <?php
    if(!$logged_in) include '../login_form.html';
    else include '../main_content.html';
    ?>
  </body>
</html>
