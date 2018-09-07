<?php
/**
* Plugin Name: HOMEINFO News
* Plugin URI: https://www.homeinfo.de/
* Description: News articles provided by HOMEINFO.
* Version: 1.1.2
**/

// Make sure we don't expose any info if called directly.
if (! function_exists('add_action')) {
    echo 'Hi there!  I\'m just a plugin, not much I can do when called directly.';
    exit;
}


require_once("settings.php");


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

    $article_template_file = plugins_url('article.html', __FILE__);
    $article_template = file_get_contents($article_template_file);
    $image_template_file = plugins_url('image.html', __FILE__);
    $image_template = file_get_contents($image_template_file);
    $news_list = json_decode($response);
    $articles = '';

    foreach ($news_list as $news) {
        $images = '';
        $title = html_entity_decode($news->title);
        $text = html_entity_decode($news->text);

        foreach ($news->images as $image) {
            $args = array('id' => $image->id, 'mimetype' => $image->mimetype);
            $query_parms = '?' . http_build_query($args);
            $image_url = plugins_url('images.php' . $query_parms, __FILE__);
            $images .= sprintf($image_template, $image_url, $image->source);
        }

        $articles .= sprintf($article_template, $title, $text, $images);
    }

    return $articles;
}


function hinews_articles_preview() {
    return 'Not implemented.';
}


function hinews_shortcode() {
    return hinews_articles();
}
?>