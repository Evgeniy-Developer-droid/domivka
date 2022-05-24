jQuery(document).ready(function ($) {

    $('#btn-avatar').click(function (){
        $('#avatar-input').click()
    })

    $('#avatar-input').change(function (e){
        let form_data = new FormData()
        let img = $(this)[0].files[0]
        form_data.append('avatar', img, img.name)
        $.ajax({
            url: urls.changeUserAvatar,
            dataType: 'json',
            cache: false,
            contentType: false,
            processData: false,
            data: form_data,
            type: 'post',
            beforeSend: function(xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            success: function (response) {
                if(response.type === 'success'){
                    $('#avatar-wrap').css('background-image', `url('${response.data.avatar}')`)
                }
            }
        });
    })


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

})