
$('#antecedentes_form').submit(function (event) {
        event.preventDefault();
        $.ajax({
        type: 'POST',
        url: $("#antecedentes_form").attr("action"),
        data: $("#antecedentes_form").serialize(), 
headers: {
        "X-CSRFToken": '{{ csrf_token }}',
},success: function(response) { 
                toastr[response.type](response.data);
        $('#antecedentes-data').empty().append(`
        <p class="fw-bold">Antecedentes Personales</p>
        <p>${response.antecedentes_personales}</p>
        <p class="fw-bold">Antecedentes Familiares</p>
        <p>${response.antecedentes_familiares}</p>
        `); 
        }});
});


