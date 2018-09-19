var cantidad_pedido = document.querySelectorAll('.cantidad_pedido');
var cantidad_entrega = document.querySelectorAll('.cantidad_entrega');
var total = document.querySelectorAll('.totalfinal');
var producto = document.querySelector('.producto_nopedido');
var presentacionxproducto = document.querySelector('.presentacionxproducto_nopedido');
var cantidad_presentacion_entrega = document.querySelector('.cantidad_presentacion_entrega_nopedido');
var total_final = document.querySelector('.total_final_nopedido');
var btn_nopedido = document.querySelector('.agregar_nopedido');
var tr_empty = document.getElementById("tr_nopedido_empty");
var tbody_nopedido = document.getElementById("tbody_nopedido");

function init_recepcion() {
    init_cantidad_entrega_blur();
    init_totalfinal_blur();
    init_prod_change();
    init_btn_nopedido();
}

function init_cantidad_entrega_blur() {
    for (var i = 0; i < cantidad_entrega.length; i++) {
        cantidad_entrega[i].addEventListener("blur", action_cantidad_entrega_blur);
        var event = new Event('blur');
        cantidad_entrega[i].dispatchEvent(event);
    }
}

function init_totalfinal_blur() {
    for (var i = 0; i < total.length; i++) {
        total[i].addEventListener("blur", action_totalfinal_blur);
    }
}

function init_prod_change() {
    $('.producto_nopedido').on("select2:selecting", function(e) {
       prod_change(this, e.params.args.data.id,e);
    });
}

function init_btn_nopedido() {
    btn_nopedido.addEventListener("click", action_btn_nopedido);
}

function action_cantidad_entrega_blur() {
    var tr_content = this.parentElement.parentElement;
    var current_cantidad_pedido = tr_content.querySelector('.cantidad_pedido');
    var color = get_color_cantidad(parseInt(current_cantidad_pedido.value), parseInt(this.value));
    var is_oferta = tr_content.querySelector('.is_oferta');
    this.style.backgroundColor = color;
    if(is_oferta.value === 'False'){
        var totalfinal = tr_content.querySelector('.totalfinal');
        var td_descuento = tr_content.querySelector('.td_descuento');
        var td_precio = tr_content.querySelector('.td_precio');
        td_precio.innerHTML = cortarNumero((parseFloat(totalfinal.value)+parseFloat(td_descuento.innerHTML))/parseFloat(this.value), 2);
    }
}

function cortarNumero(num, fixed) {
    var re = new RegExp('^-?\\d+(?:\.\\d{0,' + (fixed || -1) + '})?');
    return num.toString().match(re)[0];
}

function get_color_cantidad(pedido, entrega) {
    var color = '';
    if(pedido == entrega){
        color = '#b3e6e6';
    }else if(pedido > entrega){
        color = '#ffcdcc';
    }else{
        color = '#FACE8D';
    }
    return color;
}



function action_totalfinal_blur() {
    var tr_content = this.parentElement.parentElement;
    var current_cantidad_pedido = tr_content.querySelector('.cantidad_pedido');
    var td_descuento = tr_content.querySelector('.td_descuento');
    var td_precio = tr_content.querySelector('.td_precio');
    td_precio.innerHTML = cortarNumero((parseFloat(this.value)+parseFloat(td_descuento.innerHTML))/parseFloat(current_cantidad_pedido.value), 2);
}

function prod_change(obj, new_value,e) {
    var id_prod = new_value;
    var options_length = presentacionxproducto.options.length;
    var data = [];
    for (var i = 0; i < options_length; i++) {
        presentacionxproducto.options[0].remove();
    }
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            data = JSON.parse(xhttp.responseText);
        }
    };
    xhttp.open("GET", "/compras/api/presentacionxproducto/" + id_prod, false);
    xhttp.send();
    for (var i = 0; i < data.length; i++) {
        var opt = document.createElement('option');
        opt.value = data[i]['id'];
        opt.innerHTML = data[i]['presentacion']['descripcion'];
        presentacionxproducto.append(opt);
    }
    presentacionxproducto.value = '';
    $(presentacionxproducto).select2('open');
}

function action_btn_nopedido() {
    var producto_text = producto.options[producto.selectedIndex].text;
    var producto_val = producto.value;
    var presentacionxproducto_text = presentacionxproducto.options[presentacionxproducto.selectedIndex].text;
    var presentacionxproducto_val = presentacionxproducto.value;
    var cantidad_presentacion_entrega_val = cantidad_presentacion_entrega.value;
    var total_final_val = total_final.value;
    var temp_tr = tr_empty.cloneNode(true);
    temp_tr.removeAttribute("id");
    temp_tr.querySelector(".td_producto").innerHTML = producto_text;
    temp_tr.querySelector(".td_presentacion").innerHTML = presentacionxproducto_text;
    temp_tr.querySelector(".cantidad_presentacion_entrega_nopedido").value = cantidad_presentacion_entrega_val;
    temp_tr.querySelector(".total_final_nopedido").value = total_final;
    tbody_nopedido.appendChild(temp_tr);
}