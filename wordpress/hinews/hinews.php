<?php
/**
* Plugin Name: HOMEINFO News
* Plugin URI: https://www.homeinfo.de/
* Description: News articles provided by HOMEINFO.
* Version: 1.0.0
**/

// Make sure we don't expose any info if called directly.
if (! function_exists('add_action')) {
    echo 'Hi there!  I\'m just a plugin, not much I can do when called directly.';
    exit;
}


include("settings.php");


add_shortcode('hinews', 'hinews_shortcode');


function hinews_articles() {
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
            $query_parms = '?' . http_build_query($args);
            $image_url = plugins_url('images.php' . $query_parms, __FILE__);
            $result .= '<img src="' . $image_url . '" alt="' . $image->source . '">';
            $result .= '<br/>';
        }
    }

    return $result;
}


function hinews_shortcode() {
    return hinews_articles();
}
?>