<script lang="ts">
    import type { APIContext } from "astro";
    import { Configuration, NewValoracion, NewValoracionRequest, ResponseError, ViviendaApi } from "../api/A2viviendasREST";
    import AppConfig from "../config";
    import { getAccessToken } from "../utils/auth0";

    export let context: APIContext;
  
    let comment = "";
    let rate = 0;
    let idCasa = "";
    let userId = "";
  

    async function handleOnSubmit() {

      
      const referer = new URL(
        context.request.headers.get("referer") ?? context.url
      );

      const config = new Configuration({
        ...AppConfig.viviendas, 
        accessToken: () => getAccessToken(context)
      });
    
      const api = new ViviendaApi(config);

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
        return {
            body: JSON.stringify({
            redirect: `/houses/${idCasa}`,
            }),
        };
      } catch (e) {
        const error = e as ResponseError;
        const msg = await error.response.json().then((x) => x.detail[0]);
        return context.redirect(referer.toString());
      }
    }

  </script>
  
  <form on:submit|preventDefault={handleOnSubmit}>
    <div class="mb-3">
        <input type="text" name="idCasa" bind:value={idCasa} hidden />
        <input type="text" name="userId" bind:value={userId} hidden />
        <label for="comment" class="form-label">Comment: </label>
        <textarea bind:value={comment} name="comment" class="form-control"></textarea>
        <label for="rate" class="form-label">Rate: </label>
        <input bind:value={rate} name="rate" type="number" max="10" min="0" class="form-control"/>
        <button type="submit" class="btn btn-primary">Send</button>
    </div>    
  </form>
  