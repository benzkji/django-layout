
$.widget( "bnzk.navigation", {

    options: {
        in_time: 230,
        out_time: 100,
        _: "_"
    },

    $burger: null,
    $nav: null,
    visible: false,

    _create: function() {
        this.$burger = this.element.find("a.burger");
        this.$close = this.element.find("a.close_nav");
        this.$nav = this.element.find("nav");
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
