import type { APIContext } from "astro";
import { Configuration, NewHouseRequest, NewVivienda, ResponseError, ViviendaApi } from "../../api/A2viviendasREST";
import cookies from "../../cookies";
import AppConfig from "../../config";

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
    location: "location"
  };
  
  /**
   * Creates a new booking
   */
  export async function post(context: APIContext) {
    const referer = new URL(
        context.request.headers.get("referer") ?? context.url
    );
  
    const formData = await context.request.formData();
    //const userId = context.cookies.get(cookies.USER_ID_KEY).value;
    const userId = "HARDCODED_USERNAME";
    
    if (!userId) {
        referer.searchParams.set("danger", "User isn't log in");
        return context.redirect(referer.toString());
    }
    
  
    const config = new Configuration(AppConfig.viviendas);
    const api = new ViviendaApi(config);

    const loc : string = formData.get(FormDataKeys.location)?.toString() ?? "";

    const geoRes : GeoCodingResult = await getGeocoding(loc);

    console.log(geoRes.data);


    let newHouse : NewVivienda = {
        title: formData.get(FormDataKeys.title)?.toString() ?? "",
        description: formData.get(FormDataKeys.description)?.toString() ?? "",
        location: loc,
        userId : userId,
        latitude: geoRes.data[0].latitude,
        longitude: geoRes.data[0].longitude
    };
  
    try {
        const newHouseRequest : NewHouseRequest = {
            newVivienda : newHouse
        } 
        const response = await api.newHouse(newHouseRequest);
        return context.redirect(`/houses/${response.id}`);
        } catch (e) {
        const error = e as ResponseError;
        const msg = await error.response.json().then((x) => x.detail);
        referer.searchParams.set("danger", msg);
        return context.redirect(referer.toString());
    }
  }
  