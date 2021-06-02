import $ from 'jquery';
import widget from 'jquery-ui'


$.widget( "bnzk.menu", {

    options: {
        in_time: 230,
        out_time: 100,
        'burger_selector': '.burger',
        'close_selector': '.menu-overlay__close',
        'overlay_selector': '.menu-overlay',
        _: "_"
    },

    $burger: null,
    $close: null,
    $overlay: null,
    visible: false,

    _create: function() {
        this.$burger = this.element.find(this.options.burger_selector);
        this.$close = this.element.find(this.options.close_selector);
        this.$overlay = this.element.find(this.options.overlay_selector);
        this._on(this.$burger, {'click': this._on_toggle});
        this._on(this.$close, {'click': this.hide_nav});
        $('body').on('keyup', this.on_keyup.bind(this));
    },

    on_keyup: function(e) {
        if (e.which == 27) {
            this.hide_nav();
        }
    },

    _on_toggle: function(e) {
        if (this.visible) {
            this.hide_nav();
        } else {
            this.show_nav();
        }
    },

    show_nav: function() {
        $('body').addClass('body-overlay-visible');
        this.$overlay.addClass('menu-overlay_visible');
        this.$overlay.show(this.in_time);
        this.visible = true;
    },

    hide_nav: function() {
        $('body').removeClass('body-overlay-visible');
        this.$overlay.removeClass('menu-overlay_visible');
        this.$overlay.hide(this.out_time);
        this.visible = false;
    },

    _destroy: function(e) {

    },

});
