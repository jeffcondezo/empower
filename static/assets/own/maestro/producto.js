const deletebuttons = document.querySelectorAll('.delete');
const presentacion_to_delete = document.getElementById('presentacion_to_delete');
const addbutton = document.getElementById('add_btn');

function init_productopresentacion(){
    init_delete_buttons();
}

function init_delete_buttons() {
   for (var i = 0; i < deletebuttons.length; i++) {
        deletebuttons[i].addEventListener("click", function () {
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
        });
   }
}

function init_add_button() {
    addbutton.addEventListener("click", function () {
        var temp_tr = document.getElementById('tr_presentacion_empty');
        temp_tr.class
    });
}