'use strict';

$(function () {
  $('.js-state').change( function () {
    const url = $(this).data('url');
    const course_id = $(this).data('course_id');
    const student_id = $(this).data('student_id');
    const state = $(this).val();
    // var vote_count = $(this).siblings('.js-vote_count');
    $.ajax({
      type: 'get',
      url: url,
      dataType: 'json',
      data: {
        'course_id': course_id,
        'student_id': student_id,
        'status': state
      },
      async: true,
      success: function (data) {
        var ajax_alert = $('.ajax-alert');
        if (data.is_error){
          ajax_alert.addClass('alert-danger');
        }
        else{
          ajax_alert.addClass('alert-success');
        }
        ajax_alert.find('strong').text(data.message);
        ajax_alert.show(200).delay(2000).hide(200);
        console.log(data);
      },
      error: function () {
          $('.ajax-alert').addClass('alert-danger').show().find('strong').text('Не валидные данные');
      }
    })
  });
});

