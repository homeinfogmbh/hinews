<?php
/**
* Plugin Name: HOMEINFO News
* Plugin URI: https://www.homeinfo.de/
* Description: News articles provided by HOMEINFO.
* Version: 1.2.0
**/

// Make sure we don't expose any info if called directly.
if (! function_exists('add_action')) {
    echo 'Hi there!  I\'m just a plugin, not much I can do when called directly.';
    exit;
}


require_once("settings.php");


add_shortcode('hinews', 'hinews_shortcode');


function hinews_get_images($news, $short) {
    $image_template_file = plugins_url('image.html', __FILE__);
    $image_template = file_get_contents($image_template_file);
    $images = array();

    foreach ($news->images as $image) {
        $args = array('id' => $image->id, 'mimetype' => $image->mimetype);
        $query_parms = '?' . http_build_query($args) . '&short=' .$short;
        $image_url = plugins_url('images.php' . $query_parms, __FILE__);
        $image = sprintf($image_template, $image_url, $image->source);
        array_push($images, $image);
    }

    return $images;
}


function hinews_articles($index, $short) {
    wp_enqueue_style('hinews.css', plugins_url('hinews.css', __FILE__));
    wp_enqueue_script('hinews.js', plugins_url('hinews.js', __FILE__));
    $options = get_option('homeinfo_news_options');
    $parm_token = '?access_token=' . $options['token'];
    $base_url = 'https://backend.homeinfo.de/hinews/pub/article';
    $articles_url = $base_url . $parm_token;

    if ($index !== null) {
        $articles_url .= '&page=' . $index . '&size=1';
    }

    $response = file_get_contents($articles_url);

    if ($response === false) {
        return 'Could not load data from API. Check your credentials.';
    }

    $article_row_template_file = plugins_url('article_row.html', __FILE__);
    $article_row_template = file_get_contents($article_row_template_file);
    $article_col_template_file = plugins_url('article_col.html', __FILE__);
    $article_col_template = file_get_contents($article_col_template_file);

    if ($short) {
        $article_template_file = plugins_url('article_short.html', __FILE__);
    } else {
        $article_template_file = plugins_url('article.html', __FILE__);
    }

    $article_template = file_get_contents($article_template_file);
    $news_list = json_decode($response);
    $articles = array();
    $column_count = 3;
    $columns = array();

    foreach ($news_list as $news) {
        if ($index !== null) {
            add_filter('pre_get_document_title', function () { return $news->title; });
        }

        if (count($columns) == $column_count) {
            $columns = implode("\n", $columns);
            $article_row = sprintf($article_row_template, $columns);
            array_push($articles, $article_row);
            $columns = array();
        }

        $title = html_entity_decode($news->title);
        $images = hinews_get_images($news, $short);
        $images = implode("\n", $images);
        $text = html_entity_decode($news->text);

        if ($short) {
            $text = substr($text, 0, 150) . '...';
            $site_url = get_site_url(null, 'index.php/homeinfo-news', null);
            $article = sprintf($article_template, $title, $images, $text, $site_url);
        } else {
            $article = sprintf($article_template, $title, $images, $text);
        }

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


function hinews_shortcode($atts = [], $content = null, $tag = '') {
    if (array_key_exists('index', $atts)) {
        $index = $atts['index'];
    } else {
        $index = null;
    }

    if (array_key_exists('short', $atts)) {
        $short = true;
    } else {
        $short = false;
    }

    return hinews_articles($index, $short);
}
?>