const proveedor_id = document.getElementById('proveedor_id').value;
const detalleorden_to_save = document.getElementById('detalleorden_to_save');
const current_pos = document.getElementById("current_pos");


function init_ordencompraedit() {
    const pos = [];
    const prod = [];
    var data = [];
    for (var i = 1; i <= parseInt(current_pos.value); i++) {
        const tr = document.getElementById('tr_do_'+i);
        const prod_value = tr.querySelector('.producto').value;
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
}

function init_presentacion_select(data) {

}

function init_add_button() {
    addbutton.addEventListener("click", function () {
        var temp_tr = tr_empty.cloneNode(true);
        temp_tr.removeAttribute("id");
        var select = temp_tr.querySelector("select");
        var pos = (parseInt(current_pos.value) + 1).toString();
        select.setAttribute("name", "p"+pos+"-presentacion");
        $(select).select2({
          ajax: {
            url: '/compras/api/productoxproveedor/'+proveedor_id,
            delay: 250,
            dataType: 'json',
            processResults: function (data) {
                var result = []
                for(var i=0; i<data.length; i++){
                    result.push({'id': data[i].id, 'text': data[i].descripcion});
                }
              return {
                  results: result
              };
            }
          }
        });
        var delete_button = temp_tr.querySelector('.delete');
        current_pos.value = pos;
        delete_button.setAttribute("data-pos", pos);
        delete_button.addEventListener('click', action_delete);
        temp_tr.setAttribute("id", "row_"+pos);
        tbody_presentacion.appendChild(temp_tr);
        $(".select2-container--default").removeAttr('style').css("width","100%");
        if(presentacion_to_save.value === ""){
            presentacion_to_save.value = pos;
        }else{
            var to_save = presentacion_to_save.value.split(',');
            to_save.push(pos);
            presentacion_to_save.value = to_save.join(',');
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