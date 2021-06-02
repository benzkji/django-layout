import $ from 'jquery';
import widget from 'jquery-ui';


$.widget( "bnzk.basket_row", {

    options: {
        'overlay_selector': '.menu-overlay',
        _: "_"
    },

    $remove: null,
    $submit: null,
    $amount: null,

    _create: function() {
        this.$remove = this.element.find(".basket-list__item__remove");
        this.$submit = this.element.find('[type="submit"]');
        this.$amount = this.element.find('[type="number"]');
        this.$remove.on('click', this.on_remove.bind(this));
    },

    on_remove: function(e) {
        this.$amount.val(0);
        this.$submit.click();
    },

    _destroy: function(e) {
    },

});
