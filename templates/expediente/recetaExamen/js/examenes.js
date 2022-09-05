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
              switch(data.accion){
                case 2:
                  $('#selectExamen').fadeIn(1000).html(data);
                  let selectExamen=document.getElementById('selectExamen');
                  selectExamen.innerHTML=null
                  let elemento=""
                  data.data.map((x)=>{
                    elemento= elemento+'<option value="'+x.id_examen+'">'+x.nombre_examen+'</option>';
                  });
                  selectExamen.insertAdjacentHTML("beforeend", elemento);
                  break;
              }           
            }
  });
}