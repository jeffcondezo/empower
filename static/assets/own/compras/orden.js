var proveedor_id = document.getElementById('proveedor_id').value;
var detalleorden_to_save = document.getElementById('detalleorden_to_save');
var detalleorden_to_delete = document.getElementById('detalleorden_to_delete');
var current_pos = document.getElementById("current_pos");
var addbutton = document.getElementById("add_btn");
var tr_empty = document.getElementById("tr_detalleorden_empty");
var tbody_detalleorden = document.getElementById("tbody_detalleorden");
var btn_add_promocion = document.getElementById('add_promocion');
var btn_save_promocion = document.getElementById('save_promocion');
var div_promocion_empty = document.getElementById('div_promocion_empty');
var body_promociones = document.getElementById('body_promociones');
var div_producto_empty = document.getElementById('div_producto_empty');
var btn_promocion = document.querySelectorAll('.promocion');
var current_pos_promocion = document.getElementById('current_pos_promocion');

function init_ordencompraedit() {
    var pos = [];
    var prod = [];
    var data = [];
    for (var i = 1; i <= parseInt(current_pos.value); i++) {
        var tr = document.getElementById('tr_do_'+i);
        var prod_select = tr.querySelector('.producto');
        var prod_value = prod_select.value;
        prod_select.removeAttribute('id');
        prod_select.setAttribute('data-pos', i);
        pos.push(i);
        prod.push(prod_value);
    }
    var list_pos = pos.join(',');
    var list_prod = prod.join(',');
    detalleorden_to_save.value=list_pos;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
           data = JSON.parse(xhttp.responseText);
        }
    };
    xhttp.open("GET", "/compras/api/presentacionxproducto/"+list_prod, false);
    xhttp.send();
    init_presentacion_select(data);
    init_prod_change();
    init_pres_change();
    init_cant_blur();
    init_precio_blur();
    init_add_button();
    init_delete_button();
    init_keypress();
    init_promocion_button();
    init_addpromocion_button();
    init_save_promocion_button();
}

function init_presentacion_select(data) {
    for (var i = 0; i < data.length; i++) {
        var opt = document.createElement('option');
        opt.value = data[i]['id'];
        opt.innerHTML = data[i]['presentacion']['descripcion'];
        var select = document.getElementById('sel_pre_'+data[i]['producto']);
        select.append(opt)
    }
    var selects = document.getElementsByClassName('sel_presentacionxproducto');
    for (var i = 0; i < selects.length; i++){
        var selected = selects[i].getAttribute("data-selected");
        selects[i].value=selected;
        $(selects[i]).select2();
    }
    $(".select2-container--default").removeAttr('style').css("width","100%");
}

function init_prod_change() {
    $('.producto').on("select2:selecting", function(e) {
       prod_change(this, e.params.args.data.id,e);
    });
}
function init_pres_change() {
    $('.sel_presentacionxproducto').on("select2:selecting", function(e) {
       action_pres_change(this, e.params.args.data.id);
    });
}

function init_cant_blur() {
    var cant = document.querySelectorAll('.cantidadpresentacion');
    for (var i = 0; i < cant.length; i++) {
        cant[i].addEventListener("blur", action_cant_blur);
    }
}
function init_precio_blur() {
    var cant = document.querySelectorAll('.precio')
    for (var i = 0; i < cant.length; i++) {
        cant[i].addEventListener("blur", action_cant_blur);
    }
}
function action_cant_blur() {
    var tr = this.parentElement.parentElement;
    var precio = tr.querySelector('.precio').value;
    var cantidad = tr.querySelector('.cantidadpresentacion').value;
    if(cantidad != ''){
        var total = precio*cantidad;
        tr.querySelector('.td_total').innerHTML = total;
    }
    action_calcular_total();
}
function prod_change(obj, new_value,e) {
    var id_prod = new_value;
    if(!validar_duplicado_prod(id_prod)) {
        var current_tr = document.getElementById('tr_do_' + obj.getAttribute('data-pos'));
        var presentacion_select = current_tr.querySelector('.sel_presentacionxproducto');
        var options_length = presentacion_select.options.length;
        var data = [];
        for (var i = 0; i < options_length; i++) {
            presentacion_select.options[0].remove();
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
            presentacion_select.append(opt)
        }
        $(presentacion_select).select2('open');
    }else{
        alert('No se puede duplicar productos.')
        e.preventDefault();
    }
}
function validar_duplicado_prod(id_prod) {
    var select_prod = document.querySelectorAll('.producto');
    var resp = false;
    for (var i = 0; i < select_prod.length; i++) {
        if (id_prod == select_prod[i].value){
            resp = true;
            break;
        }
    }
    return resp
}
function action_pres_change(obj, new_value) {
    var data = [];
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            data = JSON.parse(xhttp.responseText);
            if(data.length === 0){
                data[0] = {};
                data[0]['precio_tentativo'] = 0;
            }
        }
    };
    xhttp.open("GET", "/compras/api/preciotentativo/"+new_value, false);
    xhttp.send();
    var tr = obj.parentElement.parentElement;
    tr.querySelector('.precio').value = data[0]['precio_tentativo'];
    var cantidad = tr.querySelector('.cantidadpresentacion').value;
    if(cantidad != ''){
        var total = data[0]['precio_tentativo']*cantidad;
        tr.querySelector('.td_total').innerHTML = total;
        action_calcular_total();
    }
    var cantidad_dom = tr.querySelector('.cantidadpresentacion');
    setTimeout(function(){$(cantidad_dom).focus();},0);
}

function init_add_button() {
    addbutton.addEventListener("click", function () {
        var temp_tr = tr_empty.cloneNode(true);
        temp_tr.removeAttribute("id");
        var select = temp_tr.querySelector(".producto");
        var select_presentacion = temp_tr.querySelector(".presentacionxproducto");
        var cantidad_presentacion = temp_tr.querySelector(".cantidadpresentacion");
        var precio = temp_tr.querySelector(".precio");
        var pos = (parseInt(current_pos.value) + 1).toString();
        var promocion = temp_tr.querySelector(".promocion");
        var promocion_inp = temp_tr.querySelector(".promocion_inp");
        promocion_inp.setAttribute('name', 'oferta-'+pos);
        promocion.setAttribute('data-pos', pos);
        promocion.addEventListener('click', action_btn_promocion);
        select.removeAttribute('name');
        select.setAttribute('name', 'do'+pos+'-producto');
        select.setAttribute('data-pos', pos);
        select.setAttribute('required', 'required');
        cantidad_presentacion.setAttribute('required', 'required');
        cantidad_presentacion.addEventListener("blur", action_cant_blur);
        cantidad_presentacion.removeAttribute('name');
        cantidad_presentacion.setAttribute('name', 'do'+pos+'-cantidad_presentacion');
        precio.setAttribute('required', 'required');
        precio.addEventListener("blur", action_cant_blur);
        precio.removeAttribute('name');
        precio.setAttribute('name', 'do'+pos+'-precio');
        select_presentacion.classList.add('sel_presentacionxproducto');
        select_presentacion.setAttribute('required', 'required');
        select_presentacion.removeAttribute('name');
        select_presentacion.setAttribute('name', 'do'+pos+'-presentacionxproducto');
        $(select_presentacion).select2({placeholder: "Seleccione el Producto"});
        $(select_presentacion).on("select2:selecting", function(e) {
            action_pres_change(this, e.params.args.data.id);
        });
        $(select).select2({placeholder: "Seleccione un Producto"});
        $(select).on("select2:selecting", function(e) {
            prod_change(this, e.params.args.data.id, e);
        });
        var delete_button = temp_tr.querySelector('.delete_hdn');
        current_pos.value = pos;
        delete_button.addEventListener('click', action_delete);
        temp_tr.setAttribute("id", "tr_do_"+pos);
        tbody_detalleorden.appendChild(temp_tr);
        $(".select2-container--default").removeAttr('style').css("width","100%");
        if(detalleorden_to_save.value === ""){
            detalleorden_to_save.value = pos;
        }else{
            var to_save = detalleorden_to_save.value.split(',');
            to_save.push(pos);
            detalleorden_to_save.value = to_save.join(',');
        }
        $(select).select2('open');
    });
}
function init_delete_button() {
    var delete_btns = document.getElementsByClassName('delete');
    for (var i = 0; i < delete_btns.length; i++) {
        delete_btns[i].addEventListener('click', action_delete);
    }
}

function action_delete() {
   var tr_content = this.parentElement.parentElement;
   var tr_id = tr_content.getAttribute('id');
   var pos = tr_id.split('_')[2];
   var data_id = tr_content.getAttribute('data-id');
   var current_delete = detalleorden_to_delete.value;
   var current_save = detalleorden_to_save.value;
   var array_save = current_save.split(',');
   if(data_id != null){
        if(current_delete === ''){
            detalleorden_to_delete.value = data_id;
        }else{
            var array_delete = current_delete.split(',');
            array_delete.push(id);
            detalleorden_to_delete.value = array_delete.join(',');
        }
   }
    for (var i = 0; i < array_save.length; i++) {
        if(array_save[i] === pos) {
            array_save.splice(i, 1);
        }
    }
    detalleorden_to_save.value = array_save.join(',');
    document.getElementById('tr_do_'+pos).remove();
}


function action_calcular_total() {
    var td_total = document.querySelectorAll('.td_total');
    var total = 0;
    for(var i = 0; i < td_total.length; i++){
        total += parseFloat(td_total[i].innerHTML);
    }
    document.getElementById('orden_total').innerHTML = total;
}
function init_keypress() {
    document.addEventListener('keypress', function (e) {
        if(e.keyCode == 33){
            var event = new Event('click');
            addbutton.dispatchEvent(event);
        }
    });
}

function get_decimal_separator() {
    var n = 1.1;
    n = n.toLocaleString().substring(1, 2);
    return n;
}


function init_promocion_button() {
    for (var i =0; i < btn_promocion.length; i++){
        btn_promocion[i].addEventListener('click', action_btn_promocion);
    }
}

function action_btn_promocion() {
    var pos = this.getAttribute('data-pos');
    var current_pos = current_pos_promocion.value;
    if(pos != current_pos){
        var row = body_promociones.querySelectorAll('.form-inline');
        for (var i =1; i < row.length; i++) {
            row[i].remove();
        }
        var current_tr  = document.getElementById('tr_do_'+pos);
        var promocion_inp = current_tr.querySelector('.promocion_inp');
        if(promocion_inp.value != '') {
            var promociones = JSON.parse(promocion_inp.value);
            for (var i = 0; i < promociones.length; i++) {
                var event_click = new Event('click');
                btn_add_promocion.dispatchEvent(event_click);
                var row = body_promociones.querySelectorAll('.form-inline');
                $(row[i+1].querySelector('.tipo_promocion')).val(promociones[i][0]).trigger('change').trigger('select2:selecting');
                row[i+1].querySelector('.cantidad').value = promociones[i][1];
                row[i+1].querySelector('.retorno').value = promociones[i][2];
                $(row[i+1].querySelector('.producto')).val(promociones[i][3]).trigger('change').trigger('select2:selecting');
                $(row[i+1].querySelector('.presentacion')).val(promociones[i][4]).trigger('change').trigger('select2:selecting');
            }
        }
    }
    $('#modal-promocion').modal('show');
    current_pos_promocion.value = pos;

}

function init_addpromocion_button() {
    btn_add_promocion.addEventListener('click', function () {
        var temp_div = div_promocion_empty.cloneNode(true);
        temp_div.removeAttribute("id");
        var select_tipo_promocion = temp_div.querySelector('.tipo_promocion');
        $(select_tipo_promocion).select2({placeholder: "Tipo de Promocion",dropdownParent: $('#modal-promocion')});
        temp_div.querySelector('.select2-container').style.width = "100%";
        temp_div.querySelector('.selection').style.width = "100%";
        $(select_tipo_promocion).on("select2:selecting", function(e) {
            if(e.params == undefined){
                action_change_tipoprom(this, this.value);
            }else{
                action_change_tipoprom(this, e.params.args.data.id);
            }
        });
        body_promociones.appendChild(temp_div);
    });
}

function init_save_promocion_button() {
    btn_save_promocion.addEventListener('click', function () {
        var array_content = [];
        var body_promociones = document.getElementById('body_promociones');
        var row = body_promociones.querySelectorAll('.form-inline');
        for (var i =1; i < row.length; i++){
            var temp_array = [];
            var tipo_prom = row[i].querySelector('.tipo_promocion').value;
            var cantidad = row[i].querySelector('.cantidad').value;
            var retorno = row[i].querySelector('.retorno').value;
            temp_array = temp_array.concat([tipo_prom, cantidad, retorno]);
            if (tipo_prom === "1"){
                var producto = row[i].querySelector('.producto').value;
                var presentacion = row[i].querySelector('.presentacion').value;
                temp_array = temp_array.concat([producto, presentacion]);
            }
            array_content.push(temp_array);
        }
        var current_pos = current_pos_promocion. value;
        var current_tr  = document.getElementById('tr_do_'+current_pos);
        current_tr.querySelector('.promocion_inp').value = JSON.stringify(array_content);
        $('#modal-promocion').modal('hide');
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
        var temp_selprod = div_producto_empty.querySelector('.producto').cloneNode(true);
        div_row.querySelector('.div_content_producto').appendChild(temp_selprod);
        $(temp_selprod).select2({placeholder: 'Producto oferta',dropdownParent: $('#modal-promocion')});
        $(temp_selprod).on("select2:selecting", function(e) {
            if(e.params == undefined){
                action_change_producto(this, this.value);
            }else{
                action_change_producto(this, e.params.args.data.id);
            }
        });
        temp_selprod.parentElement.querySelector('.select2-container').style.width = "100%";
        temp_selprod.parentElement.querySelector('.selection').style.width = "100%";
        var sel_presentacion = div_row.querySelector('.presentacion');
        $(sel_presentacion).select2({placeholder: 'Presentacion', dropdownParent: $('#modal-promocion')});
        sel_presentacion.parentElement.querySelector('.select2-container').style.width = "100%";
        sel_presentacion.parentElement.querySelector('.selection').style.width = "100%";
    }else{
        div_row.insertAdjacentHTML('beforeend', prom_control2);
    }
    var btn_delete = div_row.querySelector('.delete');
    btn_delete.addEventListener('click', action_delete_row);
}

function action_change_producto(obj, new_id) {
    var id_prod = new_id;
    var current_tr = obj.parentElement.parentElement;
    var presentacion_select = current_tr.querySelector('.presentacion');
    var options_length = presentacion_select.options.length;
    var data = [];
    for (var i = 0; i < options_length; i++) {
        presentacion_select.options[0].remove();
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
        presentacion_select.append(opt)
    }

}

function action_delete_row(){
    this.parentElement.parentElement.remove();
}