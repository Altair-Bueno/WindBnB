import type { APIContext } from "astro";
import { ViviendaApi } from "../../../api/A2viviendasREST";
import AppConfig from "../../../config";
import { getAccessToken } from "../../../utils/auth0";
import {
    Configuration as ValoracionConfiguration,
} from "../../../api/A2viviendasREST";

export async function post(context: APIContext) {
    const referer = new URL(
        context.request.headers.get("referer") ?? context.url
    );
    const formData = await context.request.formData();
    const idValoracion = formData.get("idValoracion")?.toString() ?? "";
    const viviendaApi = new ViviendaApi(
        new ValoracionConfiguration({
            ...AppConfig.viviendas, 
            accessToken: () => getAccessToken(context)
        })
    );

    try {
        const response = await viviendaApi.deleteValoracion({idValoracion});
        return context.redirect(
            "/?" + new URLSearchParams({ warning: "Valoration deleted" })
        );
    } catch (e) {
        return context.redirect(
            "/?" + new URLSearchParams({ danger: "Something went wrong..." })
        );
    }
}