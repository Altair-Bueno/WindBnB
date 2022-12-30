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
  
    const formData = await context.request.formData();
    console.log(formData.values.toString());

    const idCasa = formData.get("idCasa")?.toString() ?? "";
    const userId = formData.get("userId")?.toString() ?? "";
    const comment = formData.get("comment")?.toString() ?? "";
    const rate = Number(formData.get("rate")?.toString()) ?? -1;
  
    if (rate < 0 || rate > 10) {
      referer.searchParams.set("danger", "Rate must be between 0 and 10");
      return {
        body: JSON.stringify({
          redirect: `/houses/${idCasa}?danger=Rate must be between 0 and 10`,
        }),
      };
    } 

    try {
      const newValoracion: NewValoracion = {
        userId: userId,
        valoracion: rate,
        comentario: comment
      }
      const newValoracionRequest: NewValoracionRequest = {
        idCasa: idCasa,
        newValoracion: newValoracion
      }
      const response = await api.newValoracion(newValoracionRequest);
      return context.redirect(
        `/houses/${idCasa}?` + new URLSearchParams({ warning: "Thank you for your comment!" })
      );
    } catch (e) {
      const error = e as ResponseError;
      const msg = await error.response.json().then((x) => x.detail[0]);
      return context.redirect(referer.toString());
    }
  }
  