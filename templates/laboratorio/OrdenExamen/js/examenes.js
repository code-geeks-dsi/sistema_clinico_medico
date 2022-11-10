document.getElementById("selectCategoria").addEventListener("change", function(){
    listExamenes();
});

//Función para actualizar la lista de exámenes de laboratorio
function listExamenes(){
    url_agregar_cola="/laboratorio/examen/"+$('#selectCategoria').val();
    $.ajax({
            url: url_agregar_cola,
            dataType: "json",
            data: {         
            },
            success: function(data){
                  $('#selectExamen').fadeIn(1000).html(data);
                  let selectExamen=document.getElementById('selectExamen');
                  selectExamen.innerHTML=null
                  let elemento=""
                  data.data.map((x)=>{
                    elemento= elemento+'<option value="'+x.id_examen+'">'+x.nombre_examen+'</option>';
                  });
                  selectExamen.insertAdjacentHTML("beforeend", elemento);
            }
  });
}

function render_mensajes(mensajes){ 
  mensajes.forEach(mensaje => {
    if (mensaje.type!='success'){
      toastr[mensaje.type](`${mensaje.title}`,`${mensaje.data}`,{timeout: 10000});
    }else{
      toastr[mensaje.type](`${mensaje.data}`);
    }
  });
}
/**
 * Creacion: Andrea Monterrosa
 * Descripcion: funcion para cambiar el resultado a fase en proceso,
 * una ves se entrega la muestra ya no se puede eliminar
 */
function entregar_muestra_medica(id_resultado) {
  $.ajax({
    url: '/laboratorio/examen/fase/2',
    type:"POST",
    dataType: "json",
    headers: {
                  'X-CSRFToken': "{{csrf_token }}"
      }, data: {
        'id_resultado':id_resultado
      },
    success: function(data){ 
      render_mensajes(data.mensajes);
      }
    });
}