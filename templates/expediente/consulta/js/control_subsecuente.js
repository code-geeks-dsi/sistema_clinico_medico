function cargar_datos_consulta(url,id_acordeon){
    $.ajax({
    type: 'GET',
    url: url,
    data: [], 
    headers: {
            "X-CSRFToken": '${ csrf_token }',
            },
    success: function(data) { 
            consulta=data.signos_vitales.consulta;
            signos_vitales=data.signos_vitales;
            datos_consulta=`<div id="control-subsecuente-acordion-${consulta.id_consulta}" class="accordion-collapse collapse " aria-labelledby="panelsStayOpen-heading">
            <div class="accordion-body">
                <div class="row" style="margin-top: 10px;">
                    <div class="col fw-bold">
                        <p>Consulta por: </p>
                    </div>
                    <div class="col">
                        <a><textarea rows="2" cols="80" readonly>${consulta.consulta_por}</textarea></a>
                    </div>
                </div>
                <div class="row" style="margin-top: 10px;">
                    <div class="col fw-bold">
                            <p>Presente Enfermedad </p>
                    </div>
                    <div class="col">
                        <a><textarea rows="2" cols="80" readonly>${consulta.presente_enfermedad}</textarea></a>
                    </div>
                </div>
                <div class="row" style="margin-top: 10px;">
                    <div class="col fw-bold">
                            <a>Temperatura: </a>
                    </div>
                    <div class="col">
                            <a>${signos_vitales.valor_temperatura}${ signos_vitales.unidad_temperatura }</a>
                    </div>
                    <div class="col fw-bold">
                        <a>Pulso: </a>
                    </div>
                    <div class="col">
                            <a>${ signos_vitales.valor_frecuencia_cardiaca } ${ signos_vitales.unidad_frecuencia_cardiaca }</a>
                    </div>
                    <div class="col fw-bold">
                        <a>Respiraciòn: </a>
                    </div>
                    <div class="col">
                            <a>${ signos_vitales.valor_saturacion_oxigeno } ${ signos_vitales.unidad_saturacion_oxigeno } %</a>
                    </div>
                    <div class="col fw-bold">
                        <a>Presion Arterial: </a>
                    </div>
                    <div class="col">
                            <a>${ signos_vitales.valor_presion_arterial_sistolica }/${ signos_vitales.valor_presion_arterial_diastolica }</a>
                    </div>
                </div>
                    <div class="row" style="margin-top: 10px;">
                            <div class="col fw-bold">
                                    <a>Examen Fisico: </a>
                            </div>
                            <div class="col">
                                <a><textarea rows="2" cols="80" readonly>${consulta.examen_fisico}</textarea></a>
                            </div>
                    </div>
                    <div class="row" style="margin-top: 10px;">
                            <div class="col fw-bold">
                                    <a>Plan Diagnostico: </a>
                            </div>
                            <div class="col">
                                <a><textarea rows="2" cols="80" readonly>${consulta.plan_tratamiento}</textarea></a>
                            </div>
                        </div>                       
                    </div>
                </div>   
            </div>`;
            $('#'+id_acordeon).html(datos_consulta);
           
    }});
}