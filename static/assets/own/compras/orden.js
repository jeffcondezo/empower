const proveedor_id = document.getElementById('proveedor_id').value;
const detalleorden_to_save = document.getElementById('detalleorden_to_save');
const detalleorden_to_delete = document.getElementById('detalleorden_to_delete');
const current_pos = document.getElementById("current_pos");
const addbutton = document.getElementById("add_btn");
const tr_empty = document.getElementById("tr_detalleorden_empty");
const tbody_detalleorden = document.getElementById("tbody_detalleorden");

function init_ordencompraedit() {
    const pos = [];
    const prod = [];
    var data = [];
    for (var i = 1; i <= parseInt(current_pos.value); i++) {
        const tr = document.getElementById('tr_do_'+i);
        const prod_select = tr.querySelector('.producto');
        const prod_value = prod_select.value;
        prod_select.removeAttribute('id');
        prod_select.setAttribute('data-pos', i);
        pos.push(i);
        prod.push(prod_value);
    }
    const list_pos = pos.join(',');
    const list_prod = prod.join(',');
    detalleorden_to_save.value=list_pos;
    const xhttp = new XMLHttpRequest();
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
    init_add_button();
    init_delete_button();
    init_keypress();
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
    var cant = document.querySelectorAll('.cantidadpresentacion')
    for (var i = 0; i < cant.length; i++) {
        cant[i].addEventListener("blur", action_cant_blur);
    }
}
function action_cant_blur() {
    var tr = this.parentElement.parentElement;
    var precio_tentativo = tr.querySelector('.td_precio_tentativo').innerHTML;
    const cantidad = tr.querySelector('.cantidadpresentacion').value;
    if(cantidad != ''){
        const total = precio_tentativo*cantidad;
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
        const xhttp = new XMLHttpRequest();
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
    const select_prod = document.querySelectorAll('.producto');
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
    const xhttp = new XMLHttpRequest();
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
    const tr = obj.parentElement.parentElement;
    tr.querySelector('.td_precio_tentativo').innerHTML = data[0]['precio_tentativo'];
    const cantidad = tr.querySelector('.cantidadpresentacion').value;
    if(cantidad != ''){
        const total = data[0]['precio_tentativo']*cantidad;
        tr.querySelector('.td_total').innerHTML = total;
        action_calcular_total();
    }
    var cantidad_dom = tr.querySelector('.cantidadpresentacion');
    $(cantidad_dom).focus();
}

function init_add_button() {
    addbutton.addEventListener("click", function () {
        var temp_tr = tr_empty.cloneNode(true);
        temp_tr.removeAttribute("id");
        var select = temp_tr.querySelector(".producto");
        var select_presentacion = temp_tr.querySelector(".presentacionxproducto");
        var cantidad_presentacion = temp_tr.querySelector(".cantidadpresentacion");
        var pos = (parseInt(current_pos.value) + 1).toString();
        select.removeAttribute('name');
        select.setAttribute('name', 'do'+pos+'-producto');
        select.setAttribute('data-pos', pos);
        select.setAttribute('required', 'required');
        cantidad_presentacion.setAttribute('required', 'required');
        cantidad_presentacion.addEventListener("blur", action_cant_blur);
        cantidad_presentacion.removeAttribute('name');
        cantidad_presentacion.setAttribute('name', 'do'+pos+'-cantidad_presentacion_pedido');
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
    const delete_btns = document.getElementsByClassName('delete');
    for (var i = 0; i < delete_btns.length; i++) {
        delete_btns[i].addEventListener('click', action_delete);
    }
}

function action_delete() {
   const tr_content = this.parentElement.parentElement;
   const tr_id = tr_content.getAttribute('id');
   const pos = tr_id.split('_')[2];
   const data_id = tr_content.getAttribute('data-id');
   const current_delete = detalleorden_to_delete.value;
   const current_save = detalleorden_to_save.value;
   const array_save = current_save.split(',');
   if(data_id != null){
        if(current_delete === ''){
            detalleorden_to_delete.value = data_id;
        }else{
            const array_delete = current_delete.split(',');
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