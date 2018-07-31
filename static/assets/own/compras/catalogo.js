const proveedor_id = document.getElementById('proveedor_id').value;


function init_ordencompraedit() {
    init_delete_buttons();
    init_add_button();
    var pos = [];
    for (var i = 1; i <= parseInt(current_pos.value); i++) {
        pos.push(i)
    }
    presentacion_to_save.value=pos.join(',');
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