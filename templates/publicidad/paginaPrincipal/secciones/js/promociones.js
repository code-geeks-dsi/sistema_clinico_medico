let promociones;
let promocionesHtml="";

//Consultando promociones
fetch('/publicidad/inicio/publicaciones')
  .then((response) => response.json())
  .then((data) => {
    promociones=data.data;
    console.log(promociones)
    promociones.forEach(
        (promo) => {
            promocionesHtml=`${promocionesHtml} 
            <div class="card mb-3">
                <div class="row g-0">
                    <div class="col-4">
                    <!--Imagen-->
                    <img 
                        src="${promo.imagenes[0].archivo}" 
                        class="img-fluid rounded-start" 
                        alt="..."
                    >
                    </div>
                    <div class="col-8">
                    <div class="card-body">
                        <!--badge-->
                        <span class="badge bg-warning text-white">Oferta Especial</span>
                        <span class="badge bg-info text-white">${promo.servicio.nombre}</span>
                        <h5 class="card-title pt-2">Promoción</h5>
                        <p class="card-text">${promo.descripcion}</p>
                        <p class="card-text"><small class="text-muted">${promo.fecha_ultima_edicion}</small></p>
                    </div>
                    </div>
                </div>
            </div>
            `
        }
    );
    $('#load-promos').hide();
    $('#lista-promociones').append(promocionesHtml);
    console.log(promociones)
});