jQuery(document).ready(function ($) {



    $('#filter-open').click(function (){
        $('#modal-filter').removeClass('d-none')
        $('#modal-filter').addClass('d-block')
    })

    const page_obj = {page:1}

    const page_obj_init = () => {
        let url = new URL(window.location.href);
        if(url.searchParams.get("page")){page_obj.page = url.searchParams.get("page")}
        if(url.searchParams.get("city")){page_obj.city = url.searchParams.get("city")}
        if(url.searchParams.get("region")){page_obj.region = url.searchParams.get("region")}
        if(url.searchParams.get("type_real_estate")){page_obj.type_real_estate = url.searchParams.get("type_real_estate")}
        if(url.searchParams.get("rooms")){page_obj.rooms = url.searchParams.get("rooms")}
        if(url.searchParams.get("price_min")){page_obj.price_min = url.searchParams.get("price_min")}
        if(url.searchParams.get("price_max")){page_obj.price_max = url.searchParams.get("price_max")}
        if(url.searchParams.get("service_type")){page_obj.service_type = url.searchParams.get("service_type")}
    }

    const redirect = () => {
        let link = "?"
        for(let obj in page_obj){
            link += `${obj}=${page_obj[obj]}&`
        }
        window.location = window.location.origin+window.location.pathname+link
    }

    const slick_run = () => {
        $('.carousel').slick({
            slidesToShow: 3,
            slidesToScroll: 3,
            dots: true,
            infinite: false,
            appendDots: $('.slick-slider-dots'),
            responsive: [
                {
                    breakpoint: 1024,
                    settings: {
                        slidesToShow: 3,
                        slidesToScroll: 3,
                        dots: true
                    }
                },
                {
                    breakpoint: 950,
                    settings: {
                        slidesToShow: 2,
                        slidesToScroll: 2,
                        arrows: false
                    }
                },
                {
                    breakpoint: 480,
                    settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1,
                        arrows: false
                    }
                }
            ]
        });
    }

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
        let html = `<div class="col-xs-12 col-sm-4">
                        <div class="card card-custom next-page p-3 d-flex justify-content-center align-items-center">
                            <nav aria-label="..."><ul class="pagination">${html_pag}</ul></nav>
                            <div class="d-flex">
                                <button href="" class="btn btn-outline-dark m-2" id="prev_page"
                                ${response.has_previous ? "" : "disabled"}>Попередня</button>
                                <button href="" class="btn btn-outline-dark m-2" id="next_page" 
                                ${response.has_next ? "" : "disabled"}>Наступна</button>
                            </div>
                        </div>
                    </div>`;
        $("#carousel").append(html);
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
                    html += `<div class="col-xs-12 col-sm-4">
                        <div class="card card-custom" style="background-image: url('${val.thumbnail}');">
                            <div class="card-data">
                                <div class="d-flex py-3 justify-content-between"><p class="h5 text-light">${val.price} грн<p/>
                                    <a href="${val.url}" class="btn btn-sm btn-outline-light">Переглянути</a></div>
                                <div class="other">
                                    <small class="text-light">${val.city}</small>
                                    <div>
                                        <span class="badge rounded-pill text-bg-success">${type_r}</span>
                                        <span class="badge rounded-pill text-bg-info">${type_s}</span>
                                        <span title="Кімнат" class="badge rounded-pill text-bg-danger"><i class="bi bi-house-fill"></i>${val.rooms}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>`
                })
                $("#carousel").html(html);
                render_pagination(response)
                slick_run();
            },
        });
    }


    $('body').on('click', 'a.page-link', function() {
        page_obj.page = $(this).data('page');
        redirect()
    });

    $('body').on('click', '#prev_page', function() {
        page_obj.page = parseInt(page_obj.page)-1
        redirect()
    });

    $('body').on('click', '#next_page', function() {
        page_obj.page = parseInt(page_obj.page)+1
        redirect()
    });

    page_obj_init()
    render()

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