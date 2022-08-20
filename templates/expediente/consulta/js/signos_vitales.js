$('#toma_signos_vitales_form').submit(function (event) {
        event.preventDefault();
        $.ajax({
        type: 'POST',
        url: $("#toma_signos_vitales_form").attr("action"),
        data: $("#toma_signos_vitales_form").serialize(), 
        success: function(response) { 
                toastr[response.type](response.data); 
        },
        });
});
{% comment %} crear funcion para recargar signos vitales con ajax en lugar de cuando se carga la pagina {% endcomment %}