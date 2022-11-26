
import type { APIContext } from "astro";
import { EditVivienda, ViviendaApi } from "../../../api/A2viviendasREST";
import {
  Configuration as ViviendaConfiguration,
  Vivienda,
} from "../../../api/A2viviendasREST";
import AppConfig from "../../../config";

interface GeoCodingData{
    latitude : string,
    longitude: string
}

interface GeoCodingResult{
    data : GeoCodingData[];

}

async function getGeocoding(calle : string){
    return fetch(
        "http://api.positionstack.com/v1/forward?access_key=" + import.meta.env.POSITION_STACK_API_KEY + "&query=" + calle, {
            "method": "GET"
        }
    ).then(res => res.json()).then(res => {
            return res;
        }
    )
}

export async function post(context: APIContext) { 
    let viv : Vivienda;


    const referer = new URL(context.request.headers.get("referer") ?? context.url);
    const viviendaApi = new ViviendaApi(new ViviendaConfiguration(AppConfig.viviendas));

    const data = await context.request.json();
    const {
        idCasa,
        title,
        description,
        street,
        number,
        city,
        province,
        cp,
        country,
        price,
        image
    } = data;
    
    /*
    
    

    const titulo = formData.get("title")?.toString() ?? "";
    const descripcion = formData.get("description")?.toString() ?? "";
    const calle = formData.get("street")?.toString() ?? "";
    const numero = formData.get("number")?.toString() ?? "";
    const ciudad = formData.get("city")?.toString() ?? "";
    const provincia = formData.get("province")?.toString() ?? "";
    const cp = formData.get("cp")?.toString() ?? "";
    const pais = formData.get("country")?.toString() ?? "";
    const precio = formData.get("price")?.toString() ?? "";
    */

    viv = await viviendaApi.getHouseById({ idCasa });


    const loc : string = street + ", " + number + ", " + city + ", " + province + ", " + cp + ", " + country;
    const geoRes = await getGeocoding(loc);
    const lat = geoRes.data[0].latitude;
    const lon = geoRes.data[0].longitude;   


    const editVivienda : EditVivienda = {
        title : title,
        description : description,
        price: parseInt(price),
        location : loc,
        latitude : lat,
        longitude : lon,
        urlPhoto : image
    }
    try {
        const response = await viviendaApi.updateHouse({idCasa, editVivienda});
        //return context.redirect("/houses/" + idCasa + "?" + new URLSearchParams({warning: "Vivienda modificada correctamente"}));
        return {
            body: JSON.stringify({
                redirect: `/houses/${response.id}`
            })
        }
    } catch (e) {
        return context.redirect("/?" + new URLSearchParams({danger: "Algo salió mal..."}));
    }
}
