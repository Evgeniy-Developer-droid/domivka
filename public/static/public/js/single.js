jQuery(document).ready(function ($) {

  let checked = false;

  $("#check-phone").click(function (){
    if(!checked){
      $(this).text($('#phone').val())
      checked = true
      $.ajax({
        url: urls.phone_check,
        type: 'POST',
        data: {id:parseInt($('#real_id').val())},
        beforeSend: function(xhr, settings) {
          if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
          }
        },
        success: function(response){}
      });
    }
  });


  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie != '') {
      let cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        let cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }


  $('.th-custom').click(function (){
    let url = $(this).data('url')
    $('#myModal img').attr('src', url)
    $('#myModal').fadeIn()
  })

  $('.close-b').click(function (){
    $('#myModal').fadeOut()
  })

  // $('.th-custom').on('click', function() {
  //   let url = $(this).data('url')
  //   $('.imagepreview').attr('src', url);
  //   $('#imagemodal').modal('show');
  // });


})


document.addEventListener( 'DOMContentLoaded', function () {
  var main = new Splide( '#main-carousel', {
    type      : 'fade',
    rewind    : true,
    pagination: false,
    arrows    : false,
  } );


  var thumbnails = new Splide( '#thumbnail-carousel', {
    fixedWidth  : 100,
    fixedHeight : 60,
    gap         : 10,
    rewind      : true,
    pagination  : false,
    isNavigation: true,
    breakpoints : {
      600: {
        fixedWidth : 60,
        fixedHeight: 44,
      },
    },
  } );


  main.sync( thumbnails );
  main.mount();
  thumbnails.mount();

} );