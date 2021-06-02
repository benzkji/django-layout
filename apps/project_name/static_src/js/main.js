import $ from 'jquery';
import 'slick-carousel';
import 'slick-carousel/slick/slick.scss';
import 'slick-carousel/slick/slick-theme.scss';

import './menu';
import './basket_row';


export default () => {
    // $( document ).ready(function() {
    //     $("header").menu()
    // });
    $('.gallery_inner .children').slick();
    $('.page').menu();
    $('.basket-list__item').basket_row();

};
