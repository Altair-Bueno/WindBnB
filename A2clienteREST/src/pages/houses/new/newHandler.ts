import type { APIContext } from "astro";
import { Configuration, NewHouseRequest, NewVivienda, ResponseError, ViviendaApi } from "../../../api/A2viviendasREST";
import cookies from "../../../cookies";
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

export const FormDataKeys = {
    title: "title",
    description: "description",
    street: "street",
    number: "number",
    city: "city",
    province: "province",
    cp: "cp",
    country: "country",
    price: "price"
  };
  
  /**
   * Creates a new booking
   */
  export async function post(context: APIContext) {
    const referer = new URL(
        context.request.headers.get("referer") ?? context.url
    );
  
    //const formData = await context.request.formData();
   const userId = context.cookies.get(cookies.USER_ID_KEY).value;

    if (!userId) {
        referer.searchParams.set("danger", "User isn't log in");
        return context.redirect(referer.toString());
    }
    
    const config = new Configuration(AppConfig.viviendas);
    const api = new ViviendaApi(config);


    /*
    const calle = formData.get(FormDataKeys.street)?.toString() ?? "";
    const numero = formData.get(FormDataKeys.number)?.toString() ?? "";
    const ciudad = formData.get(FormDataKeys.city)?.toString() ?? "";
    const provincia = formData.get(FormDataKeys.province)?.toString() ?? "";
    const cp = formData.get(FormDataKeys.cp)?.toString() ?? "";
    const pais = formData.get(FormDataKeys.country)?.toString() ?? "";
    */

    const data = await context.request.json();
    const {
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

    const loc : string = street + ", " + number + ", " + city + ", " + province + ", " + cp + ", " + country;
    const geoRes = await getGeocoding(loc);

    
    let newHouse : NewVivienda = {
        title,
        description,
        price,
        location: loc,
        userId,
        latitude: geoRes.data[0].latitude,
        longitude: geoRes.data[0].longitude,
        urlPhoto: image
    };
    
    try {
        const newHouseRequest : NewHouseRequest = {
            newVivienda : newHouse
        } 
        const response = await api.newHouse(newHouseRequest);
        //return context.redirect(`/houses/${response.id}`);
        return {
            body: JSON.stringify({
                redirect: `/houses/${response.id}`
            })
            }
        } catch (e) {
        const error = e as ResponseError;
        const msg = await error.response.json().then((x) => x.detail[0]);
        if(msg.type === "value_error.number.not_gt"){
            referer.searchParams.set("danger", "El precio debe ser mayor que 0");
        }
        return context.redirect(referer.toString());
    }
  }
  