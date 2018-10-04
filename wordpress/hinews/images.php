<?php
// Import wordpress API.
require_once('../../../wp-load.php');


function hinews_get_image($id) {
    if (array_key_exists('mimetype', $_GET)) {
        $mimetype = $_GET['mimetype'];
    } else {
        return 'No MIME type specified.';
    }

    $options = get_option('homeinfo_news_options');
    $parm_token = '?access_token=' . $options['token'];
    $base_url = 'https://backend.homeinfo.de/hinews/pub/image/';
    $image_url = $base_url . $id . $parm_token;
    $image = file_get_contents($image_url);

    if ($image === false) {
        return 'Could not retrieve image.';
    }

    header('Content-type: ' . $mimetype);
    return $image;
}


if (array_key_exists('id', $_GET)) {
    echo hinews_get_image($_GET['id']);
}

echo 'No image ID specified.'
?>