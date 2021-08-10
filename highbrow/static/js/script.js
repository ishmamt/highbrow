$(window).on("load", function() {
    "use strict";


    //  ============= POST POPUP FUNCTION =========

    $(".create-new-post").on("click", function(){
        $(".post-popup.new-post").addClass("active");
        $(".wrapper").addClass("overlay");
        return false;
    });


    $(".post-cancel").on("click", function(){
        $(".post-popup.new-post").removeClass("active");
        $(".wrapper").removeClass("overlay");
        return false;
    });

    //  ============= POST DELETE POPUP FUNCTION =========

    $(".delete-post").on("click", function(){
        $(".delete-post-popup.new-post").addClass("active");
        $(".wrapper").addClass("overlay");
        return false;
    });
    $(".post-cancel").on("click", function(){
        $(".delete-post-popup.new-post").removeClass("active");
        $(".wrapper").removeClass("overlay");
        return false;
    });

    //  ============= SIGNIN CONTROL FUNCTION =========

    $('.sign-control li').on("click", function(){
        var tab_id = $(this).attr('data-tab');
        $('.sign-control li').removeClass('current');
        $('.sign_in_sec').removeClass('current');
        $(this).addClass('current animated fadeIn');
        $("#"+tab_id).addClass('current animated fadeIn');
        return false;
    });

    //  ============= SIGNIN TAB FUNCTIONALITY =========

    $('.signup-tab ul li').on("click", function(){
        var tab_id = $(this).attr('data-tab');
        $('.signup-tab ul li').removeClass('current');
        $('.dff-tab').removeClass('current');
        $(this).addClass('current animated fadeIn');
        $("#"+tab_id).addClass('current animated fadeIn');
        return false;
    });

    //  ============= SIGNIN SWITCH TAB FUNCTIONALITY =========

    $('.tab-feed ul li').on("click", function(){
        var tab_id = $(this).attr('data-tab');
        $('.tab-feed ul li').removeClass('active');
        $('.product-feed-tab').removeClass('current');
        $(this).addClass('active animated fadeIn');
        $("#"+tab_id).addClass('current animated fadeIn');
        return false;
    });


    //  ================== Edit Options Function =================


    $(".edit-options-open").on("click", function(){
        $(this).next(".edit-options-list").toggleClass("active");
        return false;
    });


    // ============== User Menu Script =============

    $(".user-menu-btn > a").on("click", function(){
        $("nav").toggleClass("active");
        return false;
    });


    //  ============ Notifications Open =============

    $(".notification-box-open").on("click", function(){
        $(this).next(".notification-box").toggleClass("active");
    });

    // ============= User Account Setting Open ===========

    $(".user-info").on("click", function(){
        $(this).next(".user-account-settings").toggleClass("active");
    });


});


