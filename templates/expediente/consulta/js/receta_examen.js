let id_receta_examen_eliminar="";
function set_id_receta_examen(id){
    id_receta_examen_eliminar=id;
}

//Boton para eliminar Receta
$('#eliminar-receta-examen-btn').click(()=>{
    $.ajax({
        type: 'delete',
        url: "receta-examen/",
        headers: {
          "X-CSRFToken": '{{ csrf_token }}',
          },
        data: {
            'id_receta':id_receta_examen_eliminar,
        }, 
        success: function(response) { 
            toastr[response.type](response.data);
            $('#receta-examen-'+id_receta_examen_eliminar).addClass("alert alert-danger text-decoration-line-through fw-bold");
            $('#receta-examen-opciones-'+id_receta_examen_eliminar).html("Eliminado").addClass("fst-italic");
        },
        error: function(response){
            toastr['error']('F')
        }
        });
});
