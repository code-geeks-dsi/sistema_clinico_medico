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

function add_orden(id_orden){
  $.ajax({
            url: `/laboratorio/orden/${id_orden}`,
            type:'GET',
            dataType: "json",
            data: {},
            success: function(data){ 
              toastr[data.type](`${data.data}`,`${data.title}`);      
            }
  });
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
                 elemento=`${elemento}<td><button onClick="add_orden(${Object.values(p)[0]});" class="material-symbols-outlined btn">add</button></td>`;
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


