jQuery(document).ready(function ($) {

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