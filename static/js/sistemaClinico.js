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
                const id_paciente=p.id_paciente;
                // console.log(p);
                for (const property in p) {
                  
                  elemento = elemento+'<td>'+`${p[property]==null?"":p[property]}`+'</td>';
                }
                elemento+=`<td><a href="/expediente/paciente/datos?id=${id_paciente}"><span class="material-symbols-outlined btn">edit_note</span></a></td>`;
                elemento=elemento+'<td><div onclick="accionServer('+Object.values(p)[0]+',1);"class="material-symbols-outlined btn" >add</div></td>';
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