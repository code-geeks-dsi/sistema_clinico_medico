let promociones;
let promocionesHtml="";

const detallesPromocion=(indexPromocion)=>{
    $('#cover-promo').hide();
    
    let restriccion = "";
    promociones[indexPromocion].descuentos?
        restriccion=promociones[indexPromocion].descuentos.restricciones
        :
        restriccion=""

        let imagen="";
        promociones[indexPromocion].imagenes[0]?
            imagen=`
            <img 
                src="${promociones[indexPromocion].imagenes[0].archivo}" 
                class="img-fluid rounded-start" 
                alt="..."
                style="max-height: 250px;max-width: 250px;"
            />`
            :
            imagen=`
            <img 
                src="https://cdn.pixabay.com/photo/2017/06/05/16/24/megaphone-2374502_960_720.png" 
                class="img-fluid rounded-start" 
                alt="..."
                style="max-height: 230px;max-width: 230px;"
            />`

    let detalle=`
    ${imagen}
    <div class="card-body text-center">
      <h5 class="card-title text-center"><span class="badge bg-info text-white">${promociones[indexPromocion].servicio.nombre}</span></h5>
      <p class="card-text text-center">${promociones[indexPromocion].descripcion}</p>
      <span class="badge bg-warning text-white m-2">Restricciones</span>
      <p class="card-text text-center">${restriccion}</p>
      <p class="card-text text-center text-muted fw-bold">Valido hasta el: ${promociones[indexPromocion].validez_fecha_fin}</p>
    </div>
    `
    $('#promocion-detalle').html(detalle)
    //console.log(promociones[indexPromocion])
}

//Consultando promociones
fetch('/publicidad/inicio/publicaciones')
  .then((response) => response.json())
  .then((data) => {
    promociones=data.data;
    promociones.forEach(
        (promo) => {
            let imagen="";
            promo.imagenes[0]?
                imagen=`
                <img 
                    src="${promo.imagenes[0].archivo}" 
                    class="img-fluid rounded-start" 
                    alt="..."
                />`
                :
                imagen=`
                <img 
                    src="https://cdn.pixabay.com/photo/2017/06/05/16/24/megaphone-2374502_960_720.png" 
                    class="img-fluid rounded-start" 
                    alt="..."
                />`
            promocionesHtml=`${promocionesHtml} 
            <div class="card mb-3">
                <div class="row g-0">
                    <div class="col-3">
                    <!--Imagen-->
                    ${imagen}
                    </div>
                    <div class="col-9">
                    <div class="card-body">
                        <!--badge-->
                        <span class="badge bg-warning text-white">Oferta Especial</span>
                        <span class="badge bg-info text-white">${promo.servicio.nombre}</span>
                        <h5 class="card-title pt-2">Promoción</h5>
                        <p class="card-text">${promo.descripcion}</p>
                        <div class="row">
                            <div class="col">
                                <div class="card-text" style="text-align:left;">
                                    <small class="text-muted fw-bold">última Modificación: </small>
                                </div>
                                <div class="card-text" style="text-align:left;">
                                    <small class="text-muted fw-bold">${promo.fecha_ultima_edicion}</small>
                                </div>
                            </div>
                            <div class="col">
                                <div class="text-end">
                                    <button 
                                        type="button" 
                                        class="btn btn-outline-primary"
                                        onclick="detallesPromocion(${promociones.indexOf(promo)});"    
                                    >Ver más</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    </div>
                </div>
            </div>
            `
        }
    );
    $('#load-promos').hide();
    $('#lista-promociones').append(promocionesHtml);
});