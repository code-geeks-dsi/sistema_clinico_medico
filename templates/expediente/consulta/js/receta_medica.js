//Cerrar modal de medicamentos
$('#cerar_modal_busqueda_medicamento').click(function() {
        $('#busquedaMedicamentoModal').modal('show');
});

document.getElementById("btn_agregar_a_receta").addEventListener("click",function(){
        agregarMedicamentoReceta(id_receta_medica, url_agregar_a_receta)
});
