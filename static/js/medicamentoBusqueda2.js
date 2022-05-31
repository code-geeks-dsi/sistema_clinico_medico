
//Al presionar la lupa
document.getElementById("filtro_buscar").addEventListener("click",function(){
    getDatosFiltrados(tablaData, id_component,urlFiltro, complementoConsulta);
  });
  
  function getAutocompletado(url, id_component, urlFiltro, complementoConsulta, tablaData){
      let dataAutoComletado = [];
      let consultaData = new XMLHttpRequest();
      consultaData.open("GET", url, true);
      consultaData.onload = function (e) {
        if (consultaData.readyState === 4) {
          if (consultaData.status === 200) {
              $( function() {
          
                dataAutoComletado=JSON.parse(consultaData.responseText).data
                $( "#"+id_component ).autocomplete({
                  source: dataAutoComletado,
                
            
                });
              } );
          } else {
            console.error(consultaData.statusText);
          }
        }
      };
      consultaData.onerror = function (e) {
        console.error(consultaData.statusText);
      };
      consultaData.send(null);
  }
  
  function getDatosFiltrados(tablaData, id_component, urlFiltro, complementoConsulta, id_modal){
    //Variables
    let dataTarget=document.getElementById(id_component).value;
    let resultados;
    let filtroResultado = new XMLHttpRequest();
    let complemento= complementoConsulta;
    //filtrar
    if (dataTarget != ""){
      filtroResultado.open("GET", urlFiltro+complemento+dataTarget, true);
      filtroResultado.onload = function (e) {
        if (filtroResultado.readyState === 4 && filtroResultado.status === 200) {
          resultados=JSON.parse(filtroResultado.responseText);
          tablaData.innerHTML="";
          if(resultados.data.length==0){
            tablaData.insertAdjacentHTML("beforeend", '<tr colspan="9" ><td colspan="9" style="text-align:center">No hay Resultados</td></tr>');

          }else{
            resultados.data.forEach(p => {
                //Recorre los elemntos del objeto

                let id_medicamento=p.id_medicamento;
                delete p.id_medicamento;
                let elemento='<tr>';
                for (const property in p) {
                    elemento = elemento+'<td>'+`${p[property]}`+'</td>';
                }

                //imprime los medicamentos en el modal de resultados de busqueda
                elemento=elemento+`<td>
                                    <div onclick="setMedicamento('`+id_medicamento+`');"
                                      class="material-symbols-outlined btn"
                                       >add
                                    </div>
                                  </td>`;
                elemento=elemento+'</tr>';
                tablaData.insertAdjacentHTML("beforeend", elemento);
                
            });
          }
      } else {
            console.error(filtroResultado.statusText);
      }};

      filtroResultado.onerror = function (e) {
        console.error(filtroResultado.statusText);
      };
    
      filtroResultado.send();
    }
  }
  function setMedicamento(id_medicamento){
    console.log(id_medicamento);
    $('select[name=medicamento]').val(id_medicamento);
    $('#busquedaMedicamentoModal').modal('hide')
  }
  //Funcion para agregar medicamentos a la receta
  function agregarMedicamentoReceta(id, url_data){
    $('#load').show();
  $.ajax({
            url: url_data,
            type:"POST",
            dataType: "json",
            data: {
              'medicamento':$('#id_medicamento').val(),
              'periodo_dosis': $('#id_periodo_dosis').val(),
              'unidad_periodo_dosis':$('#id_unidad_periodo_dosis').val(),
              'frecuencia_dosis': $('#id_frecuencia_dosis').val(),
              'unidad_frecuencia_dosis':$('#id_unidad_frecuencia_dosis').val(),
              'cantidad_dosis': $('#id_cantidad_dosis').val(),
              'unidad_de_medida_dosis':$('#id_unidad_de_medida_dosis').val(),
              'receta_medica': id
            },
            success: function(data){
              $('#load').hide();
                if (data.type=='warning'){
                  toastr[data.type](data.data['medicamento'][0]);   
                }
                else
                {
                  toastr[data.type](data.data);   
                }
                //document.getElementById('id_nombre_empleado').value=data[0].nombres; 
                //apellidos =  document.getElementById("id_apellido_empleado").value=data[0].apellidos;
      
                //direccion = document.getElementById("id_direccion_empleado").value=data[0].direccion;
                //$('#id_fecha_nacimiento').val(data[0].fechaNacimiento);
                //$('#id_select_sexo').val(data[0].sexo);
                //$('#id_select_rol').val(data[0].roles);

                //edit = document.getElementById("btn_editar_empleado");
                //edit.setAttribute("OnClick", "edit_Empleado("+"'"+id+"'"+");")
                //$('#login_switch').prop("checked", data[0].es_activo);
                //console.log($('input:checkbox[name=login_switch]:checked').val())

                //toastr[data.type](data.data);           
                //consultarCola(url_consulta, tablaCola);
            }
  });
  
}
  