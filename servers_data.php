<?php return array (
  0 => array(
    'name' => "Howard",
    'location' => "Хельсинки, Финляндия",
    'description' => "Стандартный сервер.<br>
      Скачивание торрентов <b>запрещено.</b>",
    'main_keys' => array_filter(explode("\n", 
      file_get_contents('../user_keys_awg/' . $username . '_howard.txt'))),
    'relay_keys' => array_filter(explode("\n", 
      file_get_contents('../user_keys_awg/' . $username .'_howard_relay.txt'))),
  ),

  1 => array(
    'name' => "Chuck",
    'location' => "Вена, Австрия",
    'description' => "Стандартный сервер.<br>
      Скачивание торрентов <b>запрещено.</b>",
    'main_keys' => array_filter(explode("\n", 
      file_get_contents('../user_keys_awg/' . $username . '_chuck.txt'))),
    'relay_keys' => array_filter(explode("\n", 
      file_get_contents('../user_keys_awg/' . $username . '_chuck_relay.txt'))),
  ),

  2 => array(
    'name' => "Jimmy",
    'location' => "Амстердам, Нидерланды",
    'description' => "Стандартный сервер.<br>
      Скачивание торрентов <b>разрешено.</b>",
    'main_keys' => array_filter(explode("\n", 
      file_get_contents('../user_keys_awg/' . $username . '_jimmy.txt'))),
    'relay_keys' => array_filter(explode("\n", 
      file_get_contents('../user_keys_awg/' . $username . '_jimmy_relay.txt'))),
  ),

  3 => array(
    'name' => "Caldera",
    'location' => "Москва, Россия",
    'description' => "Сервер для доступа к российским ресурсам из-за рубежа.<br>
      Не используйте для обхода блокировок.<br>
      Скачивание торрентов <b>запрещено.</b>",
    'main_keys' => array_filter(explode("\n", 
      file_get_contents('../user_keys_awg/' . $username . '_caldera.txt'))),
    'relay_keys' => array(),
  ),
); ?>
