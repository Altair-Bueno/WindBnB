import type { APIContext } from "astro";
import {
  Configuration,
  NewValoracion,
  NewValoracionRequest,
  ResponseError,
  ViviendaApi,
} from "../../api/A2viviendasREST";
import AppConfig from "../../config";
import { getAccessToken } from "../../utils/auth0";

export async function post(context: APIContext) {

    const referer = new URL(
      context.request.headers.get("referer") ?? context.url
    );
  
    const config = new Configuration({
      ...AppConfig.viviendas, 
      accessToken: () => getAccessToken(context)
    });
    const api = new ViviendaApi(config);
  
    const data = await context.request.json();
    const {
      idCasa,
      userId,
      comment,
      rate
    } = data;
  
    if (data.rate < 0 || data.rate > 10) {
      referer.searchParams.set("danger", "Rate must be between 0 and 10");
      return {
        body: JSON.stringify({
          redirect: `/houses/${data.idCasa}?danger=Rate must be between 0 and 10`,
        }),
      };
    } 

    try {
      const newValoracion: NewValoracion = {
        userId: data.userId,
        valoracion: data.rate,
        comentario: data.comment
      }
      const newValoracionRequest: NewValoracionRequest = {
        idCasa: data.idCasa,
        newValoracion: newValoracion
      }
      const response = await api.newValoracion(newValoracionRequest);
      return {
        body: JSON.stringify({
          redirect: `/houses/${data.idCasa}`,
        }),
      };
    } catch (e) {
      const error = e as ResponseError;
      const msg = await error.response.json().then((x) => x.detail[0]);
      return context.redirect(referer.toString());
    }
  }
  