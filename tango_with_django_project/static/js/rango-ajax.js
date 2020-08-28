$(document).ready(function () {
    $('#like_btn').click(function () {
        var categoryIdVar;
        categoryIdVar = $(this).attr('data-categoryid');

        $.get('/rango/like_category/',
            {'category_id': categoryIdVar},
            function (data) {
                $('#like_count').html(data);
                $('#like_btn').hide();
            })
    });

    $('#search-input').keyup(function () {
        var query;
        query = $(this).val();

        $.get('/rango/suggest',
            {'suggestion': query},
            function (data) {
                $('#categories-listing').html(data);
            })
    });

    $('.rango-page-add').click(function () {
        var categoryid = $(this).attr('data-categoryid');
        var title = $(this).attr('data-title');
        var url = $(this).attr('data-url');
        var clickedButton = $(this);

        $.get('/rango/search_add_page/',
            {'category_id': categoryid, 'title': title, 'url': url},
            function (data) {
                $('#page-listing').html(data);
                clickedButton.hide();
            })
    });

    if ($(window).width() < 900) {
        $('#collapseSideBar').addClass('collapse');
    } else {
        $('#collapseSideBar').removeClass('collapse');
    }

    var expandCollapse = function () {
        if ($(window).width() < 900) {
            $(function () {
                // add a class .collapse to a div .showHide
                $('#collapseSideBar').addClass('collapse');
                // set display: "" in css for the toggle button .btn.btn-primary
                // $('button.btn.btn-primary').css('display', '');// removes display property to make it visible
            });
        } else {
            $(function () {
                // remove a class .collapse from a div .showHide
                $('#collapseSideBar').removeClass('collapse');
                // set display: none in css for the toggle button .btn.btn-primary
                // $('button.btn.btn-primary').css('display', 'none');// hides button display on bigger screen
            });
        }
    }
    $(window).resize(expandCollapse); // calls the function when the window first loads
});