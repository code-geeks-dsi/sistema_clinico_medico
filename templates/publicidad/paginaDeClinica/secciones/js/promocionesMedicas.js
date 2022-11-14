let promociones;
let servicios;
let promocionesHtml="";

const detallesServicio=(indexServicio)=>{
    $('#cover-promo').hide();
    let servicio= servicios[indexServicio].servicio;
    console.log(servicio)
    
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
    $('#promocion-detalle').html(detalle)
    //console.log(promociones[indexPromocion])
}

//Consultando promociones
fetch('/publicidad/inicio/servicios')
  .then((response) => response.json())
  .then((data) => {
    servicios=data.data;
    
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
                        <span class="badge bg-info text-white">${servicio.servicio.nombre}</span>
                        <h5 class="card-title pt-2">Promoción</h5>
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
    $('#load-promos').hide();
    $('#lista-servicios').append(promocionesHtml);
});