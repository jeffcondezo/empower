const deletebuttons = document.querySelectorAll('.delete');
const presentacion_to_delete = document.getElementById('presentacion_to_delete');
const addbutton = document.getElementById('add_btn');
const tr_empty = document.getElementById("tr_presentacion_empty");
const tbody_presentacion = document.getElementById("tbody_presentacion");
const current_pos = document.getElementById("current_pos");

function init_productopresentacion(){
    init_delete_buttons();
    init_add_button();
}

function init_delete_buttons() {
   for (var i = 0; i < deletebuttons.length; i++) {
        deletebuttons[i].addEventListener("click", action_delete);
   }
}

function action_delete() {
    var id = this.getAttribute("data-id");
    var pos = this.getAttribute("data-pos");
    if (id != null){
        var presentacion_value = presentacion_to_delete.value;
        if(presentacion_value == ""){
            presentacion_to_delete.value = id;
        }else{
            var presentacion = presentacion_value.split(',');
            presentacion.push(id)
            presentacion_to_delete.value = presentacion.join();
        }

    }
    document.getElementById('row_'+pos).remove();

}

function init_add_button() {
    addbutton.addEventListener("click", function () {
        var temp_tr = tr_empty.cloneNode(true);
        temp_tr.removeAttribute("id");
        var select = temp_tr.querySelector("select");
        $(select).select2();
        var delete_button = temp_tr.querySelector('.delete');
        var pos = (parseInt(current_pos.value) + 1).toString();
        delete_button.setAttribute("data-pos", pos);
        delete_button.addEventListener('click', action_delete);
        temp_tr.setAttribute("id", "row_"+pos);
        tbody_presentacion.appendChild(temp_tr);
        $(".select2-container--default").removeAttr('style').css("width","100%");
    });
}