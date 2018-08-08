const proveedor_id = document.getElementById('proveedor_id').value;
const detalleorden_to_save = document.getElementById('detalleorden_to_save');
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
    init_add_button();
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
       prod_change(this, e.params.args.data.id);
    });
}

function prod_change(obj, new_value) {
    var id_prod = new_value;
    var current_tr = document.getElementById('tr_do_'+obj.getAttribute('data-pos'));
    var presentacion_select = current_tr.querySelector('.sel_presentacionxproducto');
    var options_length = presentacion_select.options.length;
    var data = [];
    for (var i = 0; i < options_length; i++) {
        presentacion_select.options[0].remove();
    }
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
           data = JSON.parse(xhttp.responseText);
        }
    };
    xhttp.open("GET", "/compras/api/presentacionxproducto/"+id_prod, false);
    xhttp.send();
    for (var i = 0; i < data.length; i++) {
        var opt = document.createElement('option');
        opt.value = data[i]['id'];
        opt.innerHTML = data[i]['presentacion']['descripcion'];
        presentacion_select.append(opt)
    }
}

function init_add_button() {
    addbutton.addEventListener("click", function () {
        var temp_tr = tr_empty.cloneNode(true);
        temp_tr.removeAttribute("id");
        var select = temp_tr.querySelector(".producto");
        var select_presentacion = temp_tr.querySelector(".presentacionxproducto");
        var pos = (parseInt(current_pos.value) + 1).toString();
        select.setAttribute('data-pos', pos);
        select_presentacion.classList.add('sel_presentacionxproducto');
        $(select_presentacion).select2({placeholder: "Seleccione el Producto"});
        //select.setAttribute("name", "p"+pos+"-presentacion");
        $(select).select2({placeholder: "Seleccione un Producto"});
        $(select).on("select2:selecting", function(e) {
       prod_change(this, e.params.args.data.id);
        });
        //var delete_button = temp_tr.querySelector('.delete');
        current_pos.value = pos;
        //delete_button.setAttribute("data-pos", pos);
        //delete_button.addEventListener('click', action_delete);
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
    });
}

function init_catalogoproducto_list() {
    init_submit_btn();
}

function init_submit_btn() {
    filtro_form.addEventListener("submit", function (evt) {
        evt.preventDefault();
        var id = document.getElementById('sucursal_filtro').value;
        window.location.href = "/maestro/catalogo/"+id;
    });
}