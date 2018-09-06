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


function hinews_shortcode(){
	wp_enqueue_style('hinews.css', plugins_url('hinews.css', __FILE__));
    wp_enqueue_script('hinews.js', plugins_url('js/hinews.js', __FILE__));

	$options = get_option('homeinfo_news');
	wp_localize_script('hinews.js', 'php_vars', $options);

	$template = file_get_contents(plugin_dir_path( __FILE__ )."hinews.html");
	return $template;

}
?>