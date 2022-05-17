jQuery(document).ready(function ($) {

    const render_Tooltip = (link) => {
        return `<div class="toast-container position-absolute bottom-0 end-0 p-3">
                  <div class="toast fade show" role="alert" aria-live="assertive" aria-atomic="true">
                    <div class="toast-header">
                      <strong class="me-auto">Ви впевнені?</strong>
                      <button type="button" class="btn-close btn-delete-close" data-bs-dismiss="toast" aria-label="Close"></button>
                    </div>
                    <div class="toast-body">
                      <a class="btn btn-outline-danger btn-sm" href="${link}">Видалити</a>
                    </div>
                  </div>
                </div>`
    }

    $('.delete-btn').click(function (e) {
        e.preventDefault();
        $('.toast-container').remove()
        $(this).parent().append(render_Tooltip($(this).attr('href')))
    });

    $('body').on('click', '.btn-delete-close', function (){
        $(this).parent().parent().parent().remove();
    })

    $('.btn-details-open').click(function (){
        $(this).parents('.col').children('.info-details-wrap').fadeIn();
    })
    $('.btn-details-close').click(function (){
        $(this).parents('.info-details-wrap').fadeOut()
    })

})