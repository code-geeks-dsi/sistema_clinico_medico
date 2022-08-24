function cargar_datos_consulta(id_consulta){
    $.ajax({
    type: 'GET',
    url: "{% url 'control-subsecuente-view' id_consulta=id_consulta %}",
    data: [], 
    headers: {
            "X-CSRFToken": '${ csrf_token }',
            },
    success: function(consultas) { 
            datos_consulta=``;
            contiene_consulta=ContieneConsulta.objects.filter(consulta__id_consulta=id_consulta).order_by('-fecha_de_cola').first()
            expediente=contiene_consulta.expediente_id
            contiene_consulta=list(ContieneConsulta.objects.filter(expediente_id=expediente))
            contiene_consulta.forEach((consulta)=>{
                signos_vitales=SignosVitales.objects.filter(consulta_id=contiene_consulta[i].consulta.id_consulta).order_by('-fecha').first()
                    datos_consulta+=`<div id="control-subsecuente-acordion-${consulta.id_consulta}" class="accordion-collapse collapse " aria-labelledby="panelsStayOpen-heading">
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
                                    <a>${ signo_vital.valor_frecuencia_cardiaca } ${ signo_vital.unidad_frecuencia_cardiaca } %</a>
                            </div>
                            <div class="col fw-bold">
                                <a>Presion Arterial: </a>
                            </div>
                            <div class="col">
                                    <a>${ signo_vital.valor_presion_arterial_sistolica }/${ signo_vital.valor_presion_arterial_diastolica }</a>
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
            </div>`
            });
            $('#accordion_datos_consulta').html(datos_consulta);
           
    }});
}