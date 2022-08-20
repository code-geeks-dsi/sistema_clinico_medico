function delete_nota(url) {
        $('#modal-eliminar-nota-evolucion').modal('show');
        nota_evolucion_a_eliminar=url;
}

function update_nota(id) {
        antigua_observacion=$('#observacion_evolucion_'+id).text();
        $('#modal-editar-nota-evolucion').modal('show');
        $("#id_nota_evolucion_update").val(id);
        $("#modal-editar-nota-evolucion #id_observacion").val(antigua_observacion);
}

$('#hoja-evolucion-form').submit(function (event) {
        event.preventDefault();
        $.ajax({
        type: 'POST',
        url: $("#hoja-evolucion-form").attr("action"),
        data: $("#hoja-evolucion-form").serialize(), 
        success: function(response) { 
    get_lista_notas_evolucion();
                toastr[response.type](response.data); 
        },
        });
});

$('#eliminar-nota-evolucion-btn').click(()=>{
        $.ajax({
		type: 'POST',
		url: nota_evolucion_a_eliminar,
		data: {},  
        headers: {
            "X-CSRFToken": '{{ csrf_token }}',
        },
        success: function(response){
            $('#modal-eliminar-nota-evolucion').modal('hide');
            get_lista_notas_evolucion();
			toastr[response.type](response.data); 
        }});
});

$('#hoja-evolucion-form-update').submit(function (event) {
        event.preventDefault();
        $.ajax({
        type: 'POST',
        url: $("#hoja-evolucion-form-update").attr("action"),
        data: $("#hoja-evolucion-form-update").serialize(), 
        headers: {
        "X-CSRFToken": '{{ csrf_token }}',
        },
        success: function(response){
        $('#modal-editar-nota-evolucion').modal('hide');
        get_lista_notas_evolucion();
        toastr[response.type](response.data); 
        }});
});

function get_lista_notas_evolucion() {
        $.ajax({
		type: 'GET',
		url: "{% url 'hoja-evolucion-lista' id_consulta=id_consulta %}",
		data: [], 
		success: function(response) { 
                        document.getElementById("lista-hoja-evolucion").innerHTML="";
                        data=response.data
                        data.forEach(nota => {
                                
                                document.getElementById("lista-hoja-evolucion").insertAdjacentHTML("beforeend",
                                `<div class="col mb-4">
                                <div class="card">
                                        <div class="card-header">
                                        <p class="text-muted d-flex justify-content-between">${nota.fecha_hora}<span class="material-symbols-outlined" type="button" onclick ="delete_nota('${nota.delete_url}')" >delete</span><span class="material-symbols-outlined" type="button" onclick ="update_nota(${nota.id_evolucion})" >edit</span></p>
                                        
                                        </div>
                                        <div class="card-body">
                                        <p class="card-text" id="observacion_evolucion_${nota.id_evolucion}">${nota.observacion}</p>
                                        </div>
                                </div>
                                </div>`);
                        });
                },
        });
}