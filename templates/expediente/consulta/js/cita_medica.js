//Socket Para Calendario
    let ws_scheme=window.location.protocol=='https:'?"wss":"ws";
    let socket_url=`${ws_scheme}://${window.location.host}/ws/calendario/update/`;
    const calendarioUpdateSocket=new WebSocket(socket_url);
    calendarioUpdateSocket.onmessage=(message)=>{
        
}
$('#form_crear_cita').submit(function (event) {
        event.preventDefault();
$('#load-cita').show()
        $.ajax({
        type: 'POST',
        url: $("#form_crear_cita").attr("action"),
        data: $("#form_crear_cita").serialize(), 
        headers: {
        "X-CSRFToken": '{{ csrf_token }}',
        },
        success: function(response){
        $('#load-cita').hide()
        $('#modal_agregar_cita').modal('hide');
        toastr[response.type](response.data); 
        if (response.type=='success'){
                calendarioUpdateSocket.send(JSON.stringify({
                'message':'sync'
                }));
        }
        }});
});