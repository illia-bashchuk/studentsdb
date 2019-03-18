/*window.onscroll = function(ev) {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
        alert("you're at the bottom of the page");
    }
};*/

function initJournal() {
    var indicator = $('#ajax-progress-indicator');

    $('.day-box input[type="checkbox"]').click(function (event) {
        var box = $(this);
        $.ajax(box.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'pk': box.data('student-id'),
                'date': box.data('date'),
                'present': box.is(':checked') ? '1' : '',
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            'beforeSend': function (xhr, settings) {
                indicator.show();
            },
            'error': function (xhr, status, error) {
                alert(error);
                indicator.hide();
            },
            'success': function (data, status, xhr) {
                indicator.hide();
                //alert(data['status']);
            }
        });
    });
}

$(document).ready(function () {
    initJournal();
   // initGroupSelector();
   // initDateFields();
    //initEditStudentPage();
});