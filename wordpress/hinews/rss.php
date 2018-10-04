<?php
// Import wordpress API.
require_once('../../../wp-load.php');


// function defination to convert array to xml
function array_to_xml($data, &$xml_data) {
    foreach ($data as $key => $value) {
        if (is_array($value)) {
            $subnode = $xml_data->addChild($key);
            array_to_xml($value, $subnode);
        } else {
            if (substr($key, 0, 1) === '@') {
                $xml_data->addAttribute(substr($key, 1, strlen($key)), htmlspecialchars($value));
            } else {
                $xml_data->addChild($key, htmlspecialchars($value));
            }
        }
     }
}


function hinews_get_image_urls($news) {
    $images = array();

    foreach ($news->images as $image) {
        $args = array('id' => $image->id, 'mimetype' => html_entity_decode($image->mimetype));
        $query_parms = '?' . http_build_query($args);
        $image_url = plugins_url('images.php' . $query_parms, __FILE__);
        array_push($images, $image_url);
    }

    return $images;
}


function hinews_rss_article($index, $short, $link) {
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
    $rss = array();
    $channel = array();
    $channel['title'] = $news->title;
    $text = html_entity_decode($news->text);

    if ($short) {
        $text = explode('.', $text)[0] . '.';
    }

    $channel['description'] = $text;
    $images = hinews_get_image_urls($news);
    $image = array();
    $image['url'] = $images[0];
    $image['title'] = $news->title;
    $image['link'] = $images[0];    // Makes no sense here.
    $channel['image'] = $image;
    $channel['language'] = 'de-de';

    if (! is_null($link) && ! empty($link) && $link !== '') {
        $channel['link'] = get_site_url() . '/index.php/' . $link;
    } else {
        $channel['link'] = 'https://hinews.homeinfo.de/';
    }

    $rss['channel'] = $channel;
    $xml = new SimpleXMLElement('<?xml version="1.0"?><rss></rss>');
    $xml->addAttribute('version', '2.0');
    array_to_xml($rss, $xml);
    return $xml->asXML();
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

    if (array_key_exists('link', $_GET)) {
        $link = $_GET['link'];
    } else {
        $link = null;
    }

    header('Content-Type: text/css');
    return hinews_rss_article($index, $short, $link);
}


echo hinews_rss_main();
?>