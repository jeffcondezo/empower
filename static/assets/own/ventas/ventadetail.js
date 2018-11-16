var form_pago_venta = document.getElementById('form_pago_venta');
var pago_inp = document.getElementById('pago_inp');
var total_inp = document.getElementById('total_inp');
var cliente_inp = document.getElementById('cliente_inp');
var periodo_credito = document.getElementById('periodo_credito');

function init_detail() {

    init_form_pago();
    init_tipo_pago_change();
    pago_inp.value = total_inp.value;
}

function init_form_pago() {
    form_pago_venta.addEventListener('submit', action_form_pago);
}

function action_form_pago(e) {
}

function init_tipo_pago_change() {
    $('.tipo_pago').on("select2:selecting", function(e) {
        action_tipo_pago(this, e.params.args.data.id);
    });
}
function action_tipo_pago(obj, new_value) {
    if(new_value === '1'){
        pago_inp.setAttribute('readonly', 'readonly');
        pago_inp.value = total_inp.value;
        periodo_credito.classList.add("periodo_credito_hdn");
    }else if(new_value==='2'){
        if(cliente_inp.value === ''){
            obj.value = '1';
            $(obj).trigger('select2:selecting');
        }else{
            pago_inp.removeAttribute("readonly");
            pago_inp.value = '';
            periodo_credito.classList.remove("periodo_credito_hdn");
        }
    }
}