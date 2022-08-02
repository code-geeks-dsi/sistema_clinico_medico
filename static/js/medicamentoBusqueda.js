
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
      let dosis_fields=document.getElementById('dosis_fields').childNodes;
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
              const nodeFila = document.createElement("tr");
              for (const property in p) {
                  const nodeColumna = document.createElement("td");
                  const textnode = document.createTextNode(`${p[property]}`);
                  nodeColumna.appendChild(textnode);
                  nodeFila.appendChild(nodeColumna);
              }
              dosis_fields.forEach(element => {
                if(element.nodeName!='#text'){
                  
                  const nodeColumna = document.createElement("td");
                  let clonedNode = element.cloneNode(true);
                  nodeColumna.appendChild(clonedNode);
                  nodeFila.appendChild(nodeColumna);
                }
              });
              let nodeColumna = document.createElement("td");
              nodeColumna.innerHTML=`<div class="material-symbols-outlined btn" 
                                          data-bs-toggle="modal" 
                                          data-bs-target="#modalSelectExamen">add</div>`;
              //  si la funcion set paciente existiera, pero debe ser remplazada por una para agregar dosis
              // nodeColumna.innerHTML=`<div class="material-symbols-outlined btn" 
              //                             data-bs-toggle="modal" 
              //                             data-bs-target="#modalSelectExamen"
              //                             onclick="setPaciente(${Object.values(p)[0]},
              //                                                   ${Object.values(p)[1]},
              //                                                   ${Object.values(p)[2]}, 
              //                                                   ${Object.values(p)[3]});"
              //                                                   >add</div>`;
              
              nodeFila.appendChild(nodeColumna);
              tablaData.appendChild(nodeFila);
                
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
  