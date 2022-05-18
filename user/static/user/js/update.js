jQuery(document).ready(function ($) {
    let images_wrap = `<div class="card-custom rounded-3 d-flex justify-content-center align-items-center">
                    <input type="file" accept="image/*" class="d-none addition-image">
                    <div class="bth-download btn-custom"><i class="bi bi-cloud-arrow-down-fill"></i></div>
                </div>`;
    $('.bth-add').click(function () {
        $('.addition-images-wrap .card-custom:last').before(images_wrap)
    })

    $('body').on('click', '.bth-download', function () {
        $(this).parent().children('input').click();
    })

    $('body').on('change', '.addition-image', function (e){
        let form_data = new FormData()
        let img = $(this)[0].files[0]
        let element = $(this)
        form_data.append('image', img, img.name)
        $.ajax({
            url: urls.upload_images,
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
                    let parent = element.parent();
                    parent.children('.bth-download').remove()
                    parent.css('background-color', 'none')
                    parent.css('background-image', `url(${response.data.image})`)
                    parent.append(`<input type="hidden" value="${response.data.id}" name="img_${response.data.id}"/>`)
                    parent.append(`<div class="bth-delete btn-custom"><i class="bi bi-x-circle"></i></div>`)
                }
            }
        });
    })

    $('body').on('click', '.bth-delete', function () {
        let element = $(this)
        $.ajax({
            url: urls.delete_image,
            type: 'POST',
            data: {id:parseInt(element.siblings('input[type="hidden"]').val())},
            beforeSend: function(xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            success: function(response){
                element.parent().remove()
            }
        });
    })

    $('#region').change(function (){
        $('#city').val('').change()
        $('#id_city').val('')
        $('#id_region').val($('#region option:selected').text())
    });
    $('#city').change(function (){
        $('#id_city').val($('#city option:selected').text())
    });


    $('#region').focus(function (){
        if($(this).children().length <= 1){
            get_regions_fetch()
        }
    })
    $('#city').focus(function (){
        $(this).val('').change()
        get_cities_fetch()
    })

    const get_regions_fetch = () => {
        $.ajax({
            url: urls.get_regions,
            type: 'GET',
            beforeSend: function(xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            success: function(response){
                $('#region').empty()
                $('#region').append('<option value="">Область</option>')
                response.forEach(val=>{
                    $('#region').append(`<option value="${val.normalized_name}">${val.name}</option>`)
                })
            },
        });
    }

    const get_cities_fetch = () => {
        if($('#region').val()){
            $.ajax({
                url: urls.get_cities+"?reg="+$('#region').val(),
                type: 'GET',
                beforeSend: function(xhr, settings) {
                    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                    }
                },
                success: function(response){
                    $('#city').empty()
                    $('#city').append('<option value="">Місто</option>')
                    response.forEach(val=>{
                        $('#city').append(`<option value="${val.normalized_name}">${val.name}</option>`)
                    })
                },
            });
        }
    }

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