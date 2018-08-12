var inp_precio = document.querySelectorAll('.precio');
var td_total = document.querySelectorAll('.td_total');
var td_total_compra = document.getElementById('total');
var btn_add_promocion = document.getElementById('add_promocion');
var div_promocion_empty = document.getElementById('div_promocion_empty');
var body_promociones = document.getElementById('body_promociones');

function init_ordentocompra() {
    init_precio_blur();
    init_add_button();
}

function init_precio_blur() {
    for (var i =0; i < inp_precio.length; i++){
        inp_precio[i].addEventListener('blur', action_actualizar_total);
    }
}

function action_actualizar_total() {
       var tr = this.parentElement.parentElement;
       var cantidad = tr.querySelector('.cantidad').value;
       var precio = this.value;
       var total = 0;
       tr.querySelector('.td_total').innerHTML = cantidad * precio;
       for (var i =0; i < td_total.length; i++){
           total += parseFloat(td_total[i].innerHTML);
       }
       td_total_compra.innerHTML = total;
}

function init_add_button() {
    btn_add_promocion.addEventListener('click', function () {
        var temp_div = div_promocion_empty.cloneNode(true);
        temp_div.removeAttribute("id");
        var select_tipo_promocion = temp_div.querySelector('.tipo_promocion');
        $(select_tipo_promocion).select2({placeholder: "Tipo de Promocion"});
        temp_div.querySelector('.select2-container').style.width = "100%";
        temp_div.querySelector('.selection').style.width = "100%";
        $(select_tipo_promocion).on("select2:selecting", function(e) {
            action_change_tipoprom(this, e.params.args.data.id);
        });
        body_promociones.appendChild(temp_div);
    });
}

function action_change_tipoprom(obj, new_id) {
    var div_row = obj.parentElement.parentElement;
    var div_dinamic = div_row.querySelectorAll('.div_prom_dinamico');
    for (var i =0; i < div_dinamic.length; i++){
        div_dinamic[i].remove();
    }
    if(new_id == 1){
        div_row.insertAdjacentHTML('beforeend', prom_control1);
    }else{
        div_row.insertAdjacentHTML('beforeend', prom_control2);
    }
}