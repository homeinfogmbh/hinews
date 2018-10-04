<?php
// Import wordpress API.
require_once('../../../wp-load.php');


function hinews_get_image_urls($news) {
    $images = array();

    foreach ($news->images as $image) {
        $args = array('id' => $image->id, 'mimetype' => $image->mimetype);
        $query_parms = '?' . http_build_query($args);
        $image_url = plugins_url('images.php' . $query_parms, __FILE__);
        array_push($images, $image_url);
    }

    return $images;
}


function hinews_rss_article($index, $short) {
    $options = get_option('homeinfo_news_options');
    $parm_token = '?access_token=' . $options['token'];
    $base_url = 'https://backend.homeinfo.de/hinews/pub/article';
    $articles_url = $base_url . $parm_token;
    $articles_url .= '&page=' . $index . '&size=1';
    $response = file_get_contents($articles_url);

    if ($response === false) {
        return 'Could not load data from API. Check your credentials.';
    }

    $news_list = json_decode($response);
    $news = $news_list[0];
    $rss = new SimpleXMLElement('<?xml version="1.0"?><rss></rss>');
    $channel = new SimpleXMLElement('<?xml version="1.0"?><channel></channel>');
    $channel->addChild('title', $news->title);
    $text = html_entity_decode($news->text);

    if ($short) {
        $text = explode('.', $text)[0] . '.';
    }

    $channel->addChild('description', $text);
    $images = hinews_get_image_urls($news);
    $image = new SimpleXMLElement('<?xml version="1.0"?><image></image>');
    $image->addChild('url', $images[0]);
    $image->addChild('title', 'Titelbild');
    $image->addChild('link', $images[0]);    // Makes no sense here.
    $channel->addChild('image', $image);
    $channel->addChild('language', 'de-de');
    $rss->addAttribute('version', '2.0');
    $rss->addChild('channel', $channel);
    return $rss->asXML();
}


function hinews_rss_main() {
    if (array_key_exists('index', $_GET)) {
        $index = $_GET['index'];
    } else {
        http_response_code(400);
        return 'No index specified.';
    }

    if (array_key_exists('short', $_GET)) {
        $short = $_GET['short'];
    } else {
        $short = false;
    }

    header('Content-Type: text/css');
    return hinews_rss_article($index, $short);
}


echo hinews_rss_main();
?>