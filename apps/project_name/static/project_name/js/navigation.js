
$.widget( "bnzk.navigation", {

    options: {
        in_time: 230,
        out_time: 100,
        'burger_selector': '.burger',
        'close_selector': '.close_nav',
        'nav_selector': '.nav-main',
        _: "_"
    },

    $burger: null,
    $close: null,
    $nav: null,
    visible: false,

    _create: function() {
        this.$burger = this.element.find(this.options.burger_selector);
        this.$close = this.element.find(this.options.close_selector);
        this.$nav = this.element.find(this.options.nav_selector);
        this.$burger.click($.proxy(this._on_toggle, this));
        this.$close.click($.proxy(this.hide_nav, this));
    },

    _on_toggle: function(e) {
        if (this.visible) {
            this.hide_nav();
        } else {
            this.show_nav();
        }
    },

    show_nav: function() {
        this.$nav.show(this.in_time);
        this.visible = true;
    },

    hide_nav: function() {
        this.$nav.hide(this.out_time);
        this.visible = false;
    },

    _destroy: function(e) {

    },

});
