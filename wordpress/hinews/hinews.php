<?php
/**
* Plugin Name: HOMEINFO News
* Plugin URI: https://www.homeinfo.de/
* Description: News articles provided by HOMEINFO.
* Version: 0.0.1
**/

// Make sure we don't expose any info if called directly.
if (! function_exists('add_action')) {
    echo 'Hi there!  I\'m just a plugin, not much I can do when called directly.';
    exit;
}


include("settings.php");


add_shortcode('hinews', 'hinews_shortcode');


function hinews_articles() {
    global $wp;
    wp_enqueue_style('hinews.css', plugins_url('hinews.css', __FILE__));
    wp_enqueue_script('hinews.js', plugins_url('hinews.js', __FILE__));
    $options = get_option('homeinfo_news_options');
    $parm_token = '?access_token=' . $options['token'];
    $base_url = 'https://backend.homeinfo.de/hinews/pub/article';
    $articles_url = $base_url . $parm_token;
    $response = file_get_contents($articles_url);

    if ($response === FALSE) {
        return 'Could not load data from API. Check your credentials.';
    }

    $news_list = json_decode($response);
    $result = '';

    foreach ($news_list as $news) {
        $result .= '<h2>' . $news->title . '</h2>';
        $result .= '<p>' . $news->text . '</p>';
        $result .= '<br/>';

        foreach ($news->images as $image) {
            $args = array('id' => $image->id, 'mimetype' => $image->mimetype);
            $image_url = home_url(add_query_arg($args, $wp->request));
            $result .= '<img src="' . $image_url . '" alt="' . $image->source . '">';
            $result .= '<br/>';
        }
    }

    return $result;
}


function hinews_get_image($image_id) {
    if (array_key_exists('mimetype', $_GET) {
        $mimetype = $_GET['mimetype'];
    } else {
        return 'No MIME type specified.';
    }

    $options = get_option('homeinfo_news_options');
    $parm_token = '?access_token=' . $options['token'];
    $base_url = 'https://backend.homeinfo.de/hinews/pub/image/';
    $image_url = $base_url . $image_id . $parm_token;
    header('Content-type: ' . $mimetype);
    $image = file_get_contents($articles_url);

    if ($image === FALSE) {
        return 'Could not retrieve image.';
    }

    return $image;
}


function hinews_shortcode() {
    if (array_key_exists('image', $_GET) {
        return hinews_get_image($_GET['image']);
    }

    return hinews_articles();
}
?>