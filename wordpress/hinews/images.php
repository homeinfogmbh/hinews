<?php
// Import wordpress API.
require_once('../../../wp-load.php');


function hinews_get_image($id, $short) {
    if (array_key_exists('mimetype', $_GET)) {
        $mimetype = $_GET['mimetype'];
    } else {
        return 'No MIME type specified.';
    }

    $options = get_option('homeinfo_news_options');
    $parm_token = '?access_token=' . $options['token'];
    $base_url = 'https://backend.homeinfo.de/hinews/pub/image/';
    $image_url = $base_url . $id . $parm_token;

    if ($short) {
        $image = imagecreatefromjpeg($image_url);
        $source_imagex = imagesx($image);
        $source_imagey = imagesy($image);
        $maxWidth = 350;
        $maxHeight = 150;
        $width = $maxWidth;
        $height = $maxHeight;
        $ratio = $source_imagex / $source_imagey; // width/height

        if ($width/$height < $ratio) {
            $width = $height * $ratio;
        } else {
            $height = $width / $ratio;
        }

        $dest_image = imagecreatetruecolor($maxWidth, $maxHeight);
        imagecopyresampled($dest_image, $image, 0, 0, 0, 0, $width, $height, $source_imagex, $source_imagey);
        imagejpeg($dest_image, NULL, 80);
        header("Content-Type: image/jpeg");
    } else {
        $image = file_get_contents($image_url);
        header('Content-type: ' . $mimetype);
    }

    if ($image === false) {
        return 'Could not retrieve image.';
    }

    return $image;
}


if (array_key_exists('id', $_GET)) {
    echo hinews_get_image($_GET['id'], $_GET['short']);
}

echo 'No image ID specified.'
?>