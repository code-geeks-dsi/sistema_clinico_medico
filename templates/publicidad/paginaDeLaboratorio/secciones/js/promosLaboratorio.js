let promociones;
let servicios;
let promocionesHtml="";

const HtmlPromociones=(html, publicacion, publicaciones, indexServicio)=>{
    let imagen="";
        publicacion.imagenes[0]?
                imagen=`
                <img 
                    src="${publicacion.imagenes[0].archivo}" 
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
            html=html+` 
            <div class="card mb-3" id="promo-${publicacion.id_publicacion}">
                <div class="row g-0">
                    <div class="col-3">
                    <!--Imagen-->
                    ${imagen}
                    </div>
                    <div class="col-9">
                    <div class="card-body">
                        <!--badge-->
                        <span class="badge bg-warning text-white">Oferta Especial</span>
                        <span class="badge bg-info text-white">${publicacion.servicio.nombre}</span>
                        <h5 class="card-title pt-2">Promoción</h5>
                        <p class="card-text">${publicacion.descripcion}</p>
                        <div class="row">
                            <div class="col">
                                <div class="card-text" style="text-align:left;">
                                    <small class="text-muted fw-bold">última Modificación: </small>
                                </div>
                                <div class="card-text" style="text-align:left;">
                                    <small class="text-muted fw-bold">${publicacion.fecha_ultima_edicion}</small>
                                </div>
                            </div>
                            <div class="col">
                                <div class="text-end">
                                    <button 
                                        type="button" 
                                        class="btn btn-outline-primary"
                                        onclick="detallesPromocionMedica(${indexServicio}, ${publicaciones.indexOf(publicacion)});"    
                                    >Ver más</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    </div>
                </div>
            </div>
            `
    return html;
}

const detallesPromocionMedica=(indexServicio, indexPublicacion)=>{
    $('#cover-promo').hide();
    let publicacion= servicios[indexServicio].servicio.publicaciones[indexPublicacion];
    let restriccion = "";
    //aumentando vista
    fetch(`/publicidad/inicio/vistas/${publicacion.id_publicacion}`).then((response) => response.json()).then((data) => {})
    publicacion.descuentos?
        publicacion.descuentos.restricciones
        :
        restriccion=""

        let imagen="";
        publicacion.imagenes[0]?
            imagen=`
            <img 
                src="${publicacion.imagenes[0].archivo}" 
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
      <h5 class="card-title text-center"><span class="badge bg-info text-white">${publicacion.servicio.nombre}</span></h5>
      <p class="card-text text-center">${publicacion.descripcion}</p>
      <span class="badge bg-warning text-white m-2">Restricciones</span>
      <p class="card-text text-center">${restriccion}</p>
      <p class="card-text text-center text-muted fw-bold">Valido hasta el: ${publicacion.validez_fecha_fin}</p>
      <div class="fb-share-button" data-href="https://sistema-clinico-medico.herokuapp.com/laboratorio/#promo-${publicacion.id_publicacion}" data-layout="button" data-size="large"><a target="_blank" href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fsistema-clinico-medico.herokuapp.com%2Flaboratorio%2F%23promo-${publicacion.id_publicacion}&amp;src=sdkpreparse" class="fb-xfbml-parse-ignore">Compartir</a></div>
    </div>
    `
    $('#promocion-detalle').html(detalle)
    //console.log(promociones[indexPromocion])
}

const detallesServicio=(indexServicio)=>{
    $('#cover-servicio').hide();
    let servicio= servicios[indexServicio].servicio;

    
    let restriccion = "";
    servicio.descuentos?
        restriccion=servicio.descuentos.restricciones
        :
        restriccion=""

        let imagen="";
        servicio.imagenes[0]?
            imagen=`
            <img 
                src="${servicio.imagenes[0].archivo}" 
                class="img-fluid rounded-start" 
                alt="..."
                style="max-height: 250px;max-width: 250px;"
            />`
            :
            imagen=`
            <img 
                src="https://code-geek-medic.s3.amazonaws.com/static/servicios/consultorio.png" 
                class="img-fluid rounded-start" 
                alt="..."
                style="max-height: 230px;max-width: 230px;"
            />`

    let detalle=`
    ${imagen}
    <div class="card-body text-center">
      <h5 class="card-title text-center"><span class="badge bg-info text-white">${servicio.nombre}</span></h5>
      <p class="card-text text-center">${servicio.descripcion}</p>
      <span class="badge bg-success text-white m-2">Precios</span>
      <p class="card-text text-center text-muted fw-bold">$ ${servicio.precio}</p>
    </div>
    `
    $('#servicio-detalle').html(detalle)
    //console.log(promociones[indexPromocion])
}

//Consultando promociones
fetch('/publicidad/inicio/servicios/laboratorio')
  .then((response) => response.json())
  .then((data) => {
    servicios=data.data;
    let promocionesMedicasHTML="";
    
    servicios.forEach(
        (servicio) => {
            let imagen="";
       
            servicio.servicio.imagenes[0]?
                imagen=`
                <img 
                    src="${servicio.servicio.imagenes[0].archivo}" 
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
            
            servicio.servicio.publicaciones.forEach((publicacion)=>{
                promocionesMedicasHTML= HtmlPromociones(promocionesMedicasHTML, publicacion, servicio.servicio.publicaciones, servicios.indexOf(servicio))
            })
                
            promocionesHtml=`${promocionesHtml} 
            <div class="card mb-3">
                <div class="row g-0">
                    <div class="col-4">
                    <!--Imagen-->
                    ${imagen}
                    </div>
                    <div class="col-8">
                    <div class="card-body">
                        <!--badge-->
                        <span class="badge bg-info text-white mb-3">${servicio.servicio.nombre}</span>
                        <p class="card-text">${servicio.servicio.descripcion}</p>
                        <div class="text-center">
                            <button 
                                type="button" 
                                class="btn btn-outline-primary"
                                onclick="detallesServicio(${servicios.indexOf(servicio)});"    
                            >Ver más</button>
                        </div>
                    </div>
                    </div>
                </div>
            </div>
            `
        }
    );
    //promos
    $('#load-promos-medicas').hide();
    $('#lista-promociones').append(promocionesMedicasHTML);
    
    //servicios
    $('#load-promos').hide();
    $('#lista-servicios').append(promocionesHtml);
});

