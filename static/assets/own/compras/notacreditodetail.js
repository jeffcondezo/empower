var consignar_btn = document.querySelectorAll('.consignar_btn');
var form_consigna = document.getElementById('form_consigna');


function init_detail() {
    init_consigna_btn();
}

function init_consigna_btn() {
    for (var i = 0; i < consignar_btn.length; i++) {
        consignar_btn[i].addEventListener("click", action_consigna_btn);
    }
}

function action_consigna_btn() {
    var id = this.getAttribute('data-id');
    var url = form_consigna.getAttribute('action');
    var url_array = url.split("/");
    url_array[3] = id;
    url = url_array.join("/");
    form_consigna.setAttribute('action', url);
}