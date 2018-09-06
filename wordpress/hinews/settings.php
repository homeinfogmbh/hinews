<?php

// Make sure we don't expose any info if called directly
if ( !function_exists( 'add_action' ) ) {
        echo 'Hi there!  I\'m just a plugin, not much I can do when called directly.';
        exit;
}

class HomeinfoNewsSettings {
    // Holds the values to be used in the fields callbacks
    private $options;

    public function __construct() {
        add_action('admin_menu', array($this, 'add_plugin_page') );
        add_action('admin_init', array($this, 'page_init'));
	    //fill current options
	    $this->options = get_option('homeinfo_news');
    }

    //fuegt Einstellungsseite hinzu
    public function add_plugin_page() {
        // This page will be under "Settings"
        add_options_page(
            'Settings Admin',
            'HOMEINFO News',
            'manage_options',
            'homeinfo_news',
            array($this, 'create_admin_page')
        );
    }

    //Einstellungsseite befuellen
    public function create_admin_page() {
        echo '<div class="wrap"><h1>HOMEINFO News Einstellungen</h1>';

	    if (isset( $_GET['settings-updated'])) {
		    // add settings saved message with the class of "updated"
		    add_settings_error('wporg_messages', 'wporg_message', __('Settings Saved', 'wporg'), 'updated');
	    }

        echo '<form method="post" action="options.php">';

        // This prints out all hidden setting fields
        settings_fields('homeinfo_news');
        do_settings_sections('homeinfo_news');
        submit_button();

        echo '</form></div>';
    }


    public function page_init()
    {
        register_setting(
            'HOMEINFO', // Option group
            'homeinfo_news', // Option name
            array( $this, 'sanitize' ) // Sanitize
        );

        add_settings_section(
            'setting_section_1', // ID
            'Kundenspezifische Einstellungen', // Title
            array( $this, '' ), // Callback
            'homeinfo_news' // Page
        );

        add_settings_field(
            'homeinfo_news_token', // ID
            'Token', // Title
            array($this, 'token_callback'), // Callback
            'homeinfo_news', // Page
            'setting_section_1' // Section
        );
    }

    /**
     * Sanitize each setting field as needed
     *
     * @param array $input Contains all settings fields as array keys
     */
    public function sanitize( $input ) {
        $new_input = array();

        if( isset( $input['customerId'] ) )
            $new_input['customerId'] = absint( $input['customerId'] );

	    if( isset( $input['recaptcha'] ) )
	        $new_input['recaptcha'] = htmlentities($input['recaptcha']);

        return $new_input;
    }

    /**
     * Get the settings option array and print one of its values
     */
    public function token_callback() {
	    echo '<input type="text" id="homeinfo_news_token" name="homeinfo_news[token]" value="'.$this->options['token'].'"/>';
    }
}

if( is_admin() )
    $homeinfo_news_settings = new HomeinfoNewsSettings();