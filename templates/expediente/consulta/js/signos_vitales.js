$('#toma_signos_vitales_form').submit(function (event) {
        event.preventDefault();
        $.ajax({
        type: 'POST',
        url: $("#toma_signos_vitales_form").attr("action"),
        data: $("#toma_signos_vitales_form").serialize(), 
        success: function(response) { 
                toastr[response.type](response.data); 
                $('#modal_agregar_signos_vitales').modal('hide');
                cargar_signos_vitales({{ id_consulta }});
        },
        });
});

function cargar_signos_vitales(id_consulta){
        $.ajax({
        type: 'GET',
        url: "{% url 'lista_signos_vitales' id_consulta=id_consulta %}",
        data: [], 
        headers: {
                "X-CSRFToken": '${ csrf_token }',
                },
        success: function(response) { 
                signos=``;
                response.signos_vitales.forEach((signo_vital)=>{
                        signos+=`<div class="accordion-item">
                                <h2 class="accordion-header" id="panelsStayOpen-heading-${signo_vital.id_signos_vitales}">
                                
                                        <button class="accordion-button" type="button" 
                                        data-bs-toggle="collapse" 
                                        data-bs-target="#panelsStayOpen-collapse-${signo_vital.id_signos_vitales}" aria-expanded="false" 
                                        aria-controls="panelsStayOpen-collapse-${signo_vital.id_signos_vitales}">
                                                <div class="col">
                                                        <div class="row">
                                                                <div class="col fw-bold">
                                                                <p>Fecha: </p>
                                                                </div>
                                                                <div class="col">
                                                                <p>${signo_vital.fecha}</p>
                                                                </div>
                                                        </div>
                                                        <div class="row">
                                                                <div class="col fw-bold">
                                                                <p>Responsable: </p>
                                                                </div>
                                                                <div class="col">
                                                                <p>${signo_vital.responsable_nombre} ${signo_vital.responsable_apellidos}</p>
                                                                </div>
                                                        </div>
                                                </div>
                                        </button>
                                </h2>
                                <div id="panelsStayOpen-collapse-${signo_vital.id_signos_vitales}" class="accordion-collapse collapse " 
                                aria-labelledby="panelsStayOpen-heading-${signo_vital.id_signos_vitales}">
                                
                                        <div class="accordion-body">
                                                <div class="border border-secondary rounded p-3">
        
                                                        <div class="row">
                                                                <div class="col fw-bold">
                                                                <p>Temperatura: </p>
                                                                </div>
                                                                <div class="col">
                                                                <p>${signo_vital.valor_temperatura}${ signo_vital.unidad_temperatura }</p>
                                                                </div>
                                                        </div>
                                                        <div class="row">
                                                                <div class="col fw-bold">
                                                                        <p>Frecuencia Cardiaca: </p>
                                                                </div>
                                                                <div class="col">
                                                                        <p>${ signo_vital.valor_frecuencia_cardiaca } ${ signo_vital.unidad_frecuencia_cardiaca }</p>
                                                                </div>
                                                        </div>
                                                        <div class="row">
                                                                <div class="col fw-bold">
                                                                        <p>Peso: </p>
                                                                </div>
                                                                <div class="col">
                                                                        <p>${ signo_vital.valor_peso } ${ signo_vital.unidad_peso }</p>
                                                                </div>
                                                        </div>
                                                        <div class="row">
                                                                <div class="col fw-bold">
                                                                        <p>Presión Arterial: </p>
                                                                </div>
                                                                <div class="col">
                                                                        <p>${ signo_vital.valor_presion_arterial_sistolica }/${ signo_vital.valor_presion_arterial_diastolica }</p>
                                                                </div>
                                                        </div>
                                                        <div class="row">
                                                                <div class="col fw-bold">
                                                                        <p>Saturación Oxigeno: </p>
                                                                </div>
                                                                <div class="col">
                                                                        <p>${ signo_vital.valor_saturacion_oxigeno } %</p>
                                                                </div>
                                                        </div>
                                                </div>
                                        </div>
                                </div>
                        </div>`
                });
                $('#accordion_signos_vitales').html(signos);
               
        }});
        
}