<?php
// Make sure we don't expose any info if called directly.
if (! function_exists('add_action')) {
    echo 'Hi there!  I\'m just a plugin, not much I can do when called directly.';
    exit;
}


function hinews_get_image($id) {
    $options = get_option('homeinfo_news_options');
    $parm_token = '?access_token=' . $options['token'];
    $base_url = 'https://backend.homeinfo.de/hinews/pub/image/';
    $image_url = $base_url . $id . $parm_token;
    $image file_get_contents($articles_url);

    if ($image === FALSE) {
        return 'Could not retrieve image.';
    }

    return $image;
}


hinews_get_image($_GET['id']);

?>