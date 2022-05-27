jQuery(document).ready(function (){

    const page_obj = {page:1}

    $('#region').focus(function (){
        if($(this).children().length <= 1){
            get_regions_fetch()
        }
    })
    $('#city').focus(function (){
        $(this).val('').change()
        get_cities_fetch()
    })

    const page_obj_init = () => {
        let url = new URL(window.location.href);
        get_regions_fetch(true)
        if(url.searchParams.get("page")){page_obj.page = url.searchParams.get("page")}
        if(url.searchParams.get("type_real_estate")){
            page_obj.type_real_estate = url.searchParams.get("type_real_estate")
            $('#type').val(url.searchParams.get("type_real_estate"))
        }
        if(url.searchParams.get("service_type")){
            page_obj.service_type = url.searchParams.get("service_type")
            $('#service_type').val(url.searchParams.get("service_type"))
        }
        if(url.searchParams.get("rooms")){
            page_obj.rooms = url.searchParams.get("rooms")
            $('#room').val(url.searchParams.get("rooms"))
        }
        if(url.searchParams.get("price_min")){
            page_obj.price_min = url.searchParams.get("price_min")
            $('#price-min').val(url.searchParams.get("price_min"))
        }
        if(url.searchParams.get("price_max")){
            page_obj.price_max = url.searchParams.get("price_max")
            $('#price-max').val(url.searchParams.get("price_max"))
        }
    }

    $('#city').change(function (){
        page_obj.city = $(this).val();
    })
    $('#region').change(function (){
        page_obj.region = $(this).val();
    })
    $('#type').change(function (){
        page_obj.type_real_estate = $(this).val();
    })
    $('#service_type').change(function (){
        page_obj.service_type = $(this).val();
    })
    $('#room').change(function (){
        page_obj.rooms = $(this).val();
    })
    $('#price-min').change(function (){
        page_obj.price_min = $(this).val();
    })
    $('#price-max').change(function (){
        page_obj.price_max = $(this).val();
    })

    $('form').submit(function (e){
        e.preventDefault();
        redirect()
    })


    const get_regions_fetch = (first_init = false) => {
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
                if(first_init){
                    let url = new URL(window.location.href);
                    if(url.searchParams.get("region")){
                        page_obj.region = url.searchParams.get("region")
                        $('#region').val(url.searchParams.get("region")).change()
                        get_cities_fetch(true)
                    }
                }
            },
        });
    }

    const get_cities_fetch = (first_init = false) => {
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
                    if(first_init){
                        let url = new URL(window.location.href);
                        if(url.searchParams.get("city")){
                            page_obj.city = url.searchParams.get("city")
                            $('#city').val(url.searchParams.get("city")).change()
                        }
                    }
                },
            });
        }
    }

    const render = () => {
        let link = "?"
        for(let obj in page_obj){
            link += `${obj}=${page_obj[obj]}&`
        }
        $.ajax({
            url: urls.get_real_estates+link,
            type: 'GET',
            beforeSend: function(xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            success: function(response){
                let html = ""
                response.data.forEach(val=>{
                    let type_r = val.type_real_estate === "house" ? "Дім" : val.type_real_estate === "office" ? "Офіс" : "Квартира"
                    let type_s = val.service_type === "sale" ? "Продаж" : "Оренда"
                    html += `<div class="col rounded-3">
                                <div class="card position-relative" style="padding: 4px">
                                <div class="position-absolute rounded-5 count_photos"><i class="bi bi-camera-fill"> ${val.count_photos + 1}</i></div>
                                <div class="d-flex align-items-center meta position-absolute">
                                    <span class="badge rounded-pill text-bg-success">${type_r}</span>
                                    <span class="badge rounded-pill text-bg-info">${type_s}</span>
                                    <span title="Кімнат" class="badge rounded-pill text-bg-danger"><i class="bi bi-house-fill"></i>${val.rooms}</span>
                                </div>
                                    <div class="image-thumb" style="background-image: url('${val.thumbnail}');"></div>
                                    <div class="card-data">
                                        <a href="${val.url}" class="link-light"><h5>${val.name}</h5></a>
<!--                                        <hr class="my-4" />-->
                                        <div class="d-flex align-items-center user-info">
                                                    <div class="avatar-md rounded-circle" style="background-image: url('${val.user_logo}');"></div>
                                                    <h6 class="text-light">${val.user_full_name}</h6>
                                               </div>
                                        <hr class="my-2" />
                                        <div class="row">
                                            <div class="col">
                                                <div class="p-2 rounded-5 price"><b>${val.price}</b> грн${val.service_type === "sale" ? "" : "/місяць"}</div>
                                                <small class="text-light">${val.city}</small>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>`
                    $('#items-wrap').html(html)
                    render_pagination(response)
                })

            },
        });
    }

    page_obj_init()
    render()


    const redirect = () => {
        let link = "?"
        for(let obj in page_obj){
            link += `${obj}=${page_obj[obj]}&`
        }
        window.location = window.location.origin+"/catalog/"+link
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

    $('body').on('click', 'a.page-link', function() {
        page_obj.page = $(this).data('page');
        redirect()
    });

    const render_pagination = (response) => {
        let html_pag = "";
        let dots = true;
        let now = response.now_page
        let count = response.count_pages
        for(let i = 1; i <= count; i++){
            if(i === 1 || i === 2 || i-1 === now || i+1 === now || i === now || i === count|| i+1 === count){
                if(i === now){
                    html_pag += `<li class="page-item active"><a class="page-link" data-page="${i}" href="#">${i}</a></li>`
                }else{
                    html_pag += `<li class="page-item"><a class="page-link" data-page="${i}" href="#">${i}</a></li>`
                }
                dots = true
            }else{
                if(dots){
                    html_pag += "<span>...</span>"
                    dots = false
                }
            }
        }
        $(".pagination-items").html(`<nav aria-label="..."><ul class="pagination">${html_pag}</ul></nav>`);
    }



    $('.filter-btn').click(()=>{
        if($('.filter').hasClass('filter-down')){
            $('.filter').removeClass('filter-down')
            $('.filter').addClass('filter-up')
        }else{
            $('.filter').removeClass('filter-up')
            $('.filter').addClass('filter-down')
        }
    })

})