<?php
/**
* Plugin Name: HOMEINFO News
* Plugin URI: https://www.homeinfo.de/
* Description: News articles provided by HOMEINFO.
* Version: 1.1.8
**/

// Make sure we don't expose any info if called directly.
if (! function_exists('add_action')) {
    echo 'Hi there!  I\'m just a plugin, not much I can do when called directly.';
    exit;
}


require_once("settings.php");


add_shortcode('hinews', 'hinews_shortcode');


function hinews_get_images($news) {
    $image_template_file = plugins_url('image.html', __FILE__);
    $image_template = file_get_contents($image_template_file);
    $images = array();

    foreach ($news->images as $image) {
        $args = array('id' => $image->id, 'mimetype' => $image->mimetype);
        $query_parms = '?' . http_build_query($args);
        $image_url = plugins_url('images.php' . $query_parms, __FILE__);
        $image = sprintf($image_template, $image_url, $image->source);
        array_push($images, $image);
    }

    return $images;
}


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

    $article_row_template_file = plugins_url('article_row.html', __FILE__);
    $article_row_template = file_get_contents($article_row_template_file);
    $article_col_template_file = plugins_url('article_col.html', __FILE__);
    $article_col_template = file_get_contents($article_col_template_file);
    $article_template_file = plugins_url('article.html', __FILE__);
    $article_template = file_get_contents($article_template_file);
    $news_list = json_decode($response);
    $articles = array();
    $column_count = 3;
    $columns = array();

    foreach ($news_list as $news) {
        if (count($columns) == $column_count) {
            $columns = implode("\n", $columns);
            $article_row = sprintf($article_row_template, $columns);
            array_push($articles, $article_row);
            $columns = array();
        }

        $images = hinews_get_images($news);
        $images = implode("\n", $images);
        $title = html_entity_decode($news->title);
        $text = html_entity_decode($news->text);
        $article = sprintf($article_template, $title, $images, $text);
        $column = sprintf($article_col_template, $article);
        array_push($columns, $column);
    }

    if (count($columns) > 0) {
        $columns = implode("\n", $columns);
        $article_row = sprintf($article_row_template, $columns);
        array_push($articles, $article_row);
        $columns = array();
    }

    return implode("\n", $articles);
}


function hinews_articles_preview() {
    return 'Not implemented.';
}


function hinews_shortcode() {
    return hinews_articles();
}
?>