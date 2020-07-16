$(document).ready(function () {
    $('#like_btn').click(function () {
        var categoryIdVar;
        // data-categoryid is extracted from the button's data-categoryid attribute
        // it is populated by Django template engine with unique ID of category when page is rendered
        categoryIdVar = $(this).attr('data-categoryid');

        // $.get is JQuery function that handles AJAX get requests
        $.get('/rango/like_category/',
            {'category_id': categoryIdVar},
            function (data) {
                $('#like_count').html(data);
                $('#like_btn').hide();
            })
    });

    // when user types letter into search box, this function happens each time
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
});