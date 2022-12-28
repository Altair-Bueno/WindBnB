import { APIContext } from "astro";
import Cookies from "../../cookies";
import axios from 'axios';


export async function get(context: APIContext) {
    const url = new URL(context.request.url);
    const code = url.searchParams.get("code");

    /*
        POST https://YOUR_DOMAIN/oauth/token
        Content-Type: application/x-www-form-urlencoded

        grant_type=authorization_code&
        client_id=YOUR_CLIENT_ID&
        client_secret=YOUR_CLIENT_SECRET&
        code=AUTHORIZATION_CODE&
        redirect_uri=https://YOUR_APP/callback
    */

    const payload = new URLSearchParams();
    payload.append("grant_type", "authorization_code");
    payload.append("client_id", import.meta.env.PUBLIC_AUTH_CLIENT_ID);
    payload.append("client_secret", import.meta.env.AUTH_CLIENT_SECRET);
    payload.append("code", code?.toString() ?? "");
    payload.append("redirect_uri", import.meta.env.PUBLIC_AUTH_REDIRECT_URL);
    const response = await fetch("https://" + import.meta.env.PUBLIC_AUTH_DOMAIN_URL + "/oauth/token", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: payload.toString(),
    }).then((x) => x.json());

    const access_token = response?.access_token;
    context.cookies.set(Cookies.USER_ID_KEY, access_token?.toString() ?? "", { path: "/" });

    //Validate token:
    const options = {
        headers: {
          Authorization: `Bearer ${access_token}`
        }
    };

    /*
    curl -X 'GET' \
    --url 'http://127.0.0.1:8000/api/private' \
    --header  'Authorization: Bearer <YOUR_BEARER_TOKEN>'
    */

    let res = await fetch(
        "http://localhost:8000/validate", 
        {
            method: "GET",
            headers: {
                "Content-Type": "text/plain; charset=UTF-8",
                "Authorization": `Bearer ${access_token}`
            }
        }
   )

   console.log(res)
      
    /*
    // Realizar la solicitud HTTP
    await axios.get("http://localhost:8000/validate", options)
    .then(function (response) {
        // Procesar la respuesta del servidor
        const data = response.data;
        console.log(data);
        // Hacer algo con los datos de la respuesta
    })
    .catch(function (error) {
        console.log(error);
    });
    */

    return context.redirect("/");
}
