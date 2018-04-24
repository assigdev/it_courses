'use strict';

$(function () {
  $('.js-state').change( function () {
    const course_id = $(this).data('course_id');
    const student_id = $(this).data('student_id');
    const csrf_token = $(this).data('csrf_token');
    const state = $(this).val();
    $.ajax({
      type: 'post',
      dataType: 'json',
      data: {
        'course_id': course_id,
        'student_id': student_id,
        'status': state,
        'csrfmiddlewaretoken': csrf_token
      },
      async: true,
      success: success_func,
      error: error_func
    })
  });

  $('.js-ajax-send').click( function () {
      var form = $(this).parent();
      console.log(form.serialize());
    $.ajax({
      type: 'post',
      dataType: 'json',
      data: form.serialize(),
      async: true,
      success: success_func,
      error: error_func
    })
  });
});

function success_func(data) {
    var ajax_alert = $('.ajax-alert');
        if (data.is_error){
          ajax_alert.removeClass('alert-success').addClass('alert-danger');
        }
        else{
          ajax_alert.removeClass('alert-danger').addClass('alert-success');
        }
        ajax_alert.find('strong').text(data.message);
        ajax_alert.show(200).delay(1000).hide(200);
        console.log(data);
}

function error_func() {
    $('.ajax-alert').addClass('alert-danger').show().find('strong').text('Сервер не отвечает');
}