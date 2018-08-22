var cantidad = document.querySelectorAll('.cantidad');
var total = document.querySelectorAll('.totalfinal');

function init_recepcion() {
    init_check_cantidad();
    init_check_cantidad_oferta();
    init_cantidad_blur();
    init_totalfinal_blur();
}

function init_check_cantidad() {
    $(document).on('change', '[data-change="check-conforme"]', action_check_cantidad);
}

function init_check_cantidad_oferta() {
    $(document).on('change', '[data-change="check-oferta-conforme"]', action_check_cantidad_oferta);
}
function init_cantidad_blur() {
    for (var i = 0; i < cantidad.length; i++) {
        cantidad[i].addEventListener("blur", action_cantidad_blur);
    }
    
}
function action_check_cantidad() {
    var tr_content = this.parentElement.parentElement.parentElement;
    if(this.checked) {
        tr_content.querySelector('.cantidad').setAttribute("readonly", "readonly");
        tr_content.querySelector('.totalfinal').setAttribute("readonly", "readonly");
    }else{
        tr_content.querySelector('.cantidad').removeAttribute("readonly");
        tr_content.querySelector('.totalfinal').removeAttribute("readonly");
    }
}
function action_check_cantidad_oferta() {
    var tr_content = this.parentElement.parentElement.parentElement;
    if(this.checked) {
        tr_content.querySelector('.cantidad_promocion').setAttribute("readonly", "readonly");
    }else{
        tr_content.querySelector('.cantidad_promocion').removeAttribute("readonly");
    }
}

function action_cantidad_blur() {
    var tr_content = this.parentElement.parentElement;
    var precio = tr_content.querySelector('.td_precio').innerHTML;
    tr_content.querySelector('.totalfinal').value = this.value * precio;
}

function init_totalfinal_blur() {
    for (var i = 0; i < total.length; i++) {
        total[i].addEventListener("blur", action_totalfinal_blur);
    }
}

function action_totalfinal_blur() {
    var tr_content = this.parentElement.parentElement;
    var cantidad = tr_content.querySelector('.cantidad').value;
    tr_content.querySelector('.td_precio').innerHTML = this.value / cantidad;
}