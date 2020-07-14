// $(document).ready(function () {
//     console.log("Simple ready function for jQuery complete.");
// });

$(document).ready(function () {
    // the '#' is for unique identifier
    // when the msg element is found, add 'ooo, fancy!' at the end.  
    $('#about-btn').click(function () {
        msgStr = $('#msg').html();
        msgStr = msgStr + " ooo, fancy!";

        $('#msg').html(msgStr);
    });

    // the '.' is for an id, where it is a group of elements.
    $('.ouch').click(function () {
        alert('You clicked me! Ouch!');
    });

    // this is for tag name, so any of an entire element will get these traits
    // NOTE that if you change the 'this' to 'p', then all elements tagged as 'p' will change at once
    $('p').hover(
        function () {
            $(this).css('color', 'red');
        },
        function () {
            $(this).css('color', 'black');
        });
});

// $() is used to access jQuery framework, all using jQuery has this.
// $(document) = selector, select the HTML document object.
// read() is used by the selected document by chaining that function onto our selector
// only executed when DOM page is fully loaded in memory.
// function() is an anonymous function when DOM is ready to go.

// NOTE: jQuery is function programming style, as opposed to JS which is procedural.  All jQuery commands do this:
// Select and Act.  Select an element, perform some action with element.