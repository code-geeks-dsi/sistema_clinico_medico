document.getElementById("selectCategoria").addEventListener("change", function(){

  accionServer($('#selectCategoria').val(), 2);
  console.log($('#selectCategoria').val());
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
                let elemento='<tr>';
                for (const property in p) {
                    elemento = elemento+'<td>'+`${p[property]}`+'</td>';
                }

                //imprime paciente en el modal de resultados de busqueda
                elemento=elemento+'<td><div onclick="setPaciente('+Object.values(p)[0]+','+"'"+Object.values(p)[1]+"', '"+Object.values(p)[2]+"', "+"'"+Object.values(p)[3]+"'"+');"class="material-symbols-outlined btn" data-bs-toggle="modal" data-bs-target="#modalSelectExamen" >add</div></td>';
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

function setPaciente(id_paciente, nombre_paciente, apellido_paciente, fecha_nacimiento){
  edad=getEdad(fecha_nacimiento);
  $('#pacienteId').val(id_paciente);
  $('#nombrePaciente').val(nombre_paciente+" "+apellido_paciente);
  $('#edadPaciente').val(edad +" años")
  

}
function getEdad(dateString) {
  let hoy = new Date()
  let fechaNacimiento = new Date(dateString)
  let edad = hoy.getFullYear() - fechaNacimiento.getFullYear()
  let diferenciaMeses = hoy.getMonth() - fechaNacimiento.getMonth()
  if (
    diferenciaMeses < 0 ||
    (diferenciaMeses === 0 && hoy.getDate() < fechaNacimiento.getDate())
  ) {
    edad--
  }
  return edad
}


