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


function hinews_shortcode(){
    wp_enqueue_style('hinews.css', plugins_url('hinews.css', __FILE__));
    wp_enqueue_script('hinews.js', plugins_url('hinews.js', __FILE__));
    $options = get_option('homeinfo_news_options');
    wp_localize_script('hinews.js', 'php_vars', $options);
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
            $image_url = plugins_url('images.php?id=' . $image->id, __FILE__);
            $result .= '<img src="' . $image_url . '" alt="' . $image->source . '">';
            $result .= '<br/>';
        }
    }

    return $result;
}
?>