import type { APIContext } from "astro";
import { ViviendaApi } from "../../../api/A2viviendasREST";
import {
  Configuration as ViviendaConfiguration,
  Vivienda,
} from "../../../api/A2viviendasREST";
import AppConfig from "../../../config";

export async function post(context: APIContext) {
  const referer = new URL(
    context.request.headers.get("referer") ?? context.url
  );
  const formData = await context.request.formData();
  const idCasa = formData.get("idCasa")?.toString() ?? "";
  const viviendaApi = new ViviendaApi(
    new ViviendaConfiguration(AppConfig.viviendas)
  );

  try {
    const response = await viviendaApi.deleteHouse({ idCasa });
    return context.redirect(
      "/?" + new URLSearchParams({ warning: "House deleted" })
    );
  } catch (e) {
    return context.redirect(
      "/?" + new URLSearchParams({ danger: "Something went wrong..." })
    );
  }
}
