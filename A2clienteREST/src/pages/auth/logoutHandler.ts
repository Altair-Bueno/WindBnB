import type { APIContext } from "astro";
import Cookies from "../../cookies";

export const URI = "/auth/logoutHandler";

export const FormDataKeys = {
  origin: "origin",
};

export async function post(context: APIContext) {
  context.cookies.delete(Cookies.USER_ID_KEY, { path: "/" });
  
  /*
    GET https://YOUR_DOMAIN/v2/logout?
    client_id=YOUR_CLIENT_ID&
    returnTo=LOGOUT_URL
  */
  
  const url = await context.request
  .formData()
  .then((x) => x.get(FormDataKeys.origin));

  const payload = new URLSearchParams();
  payload.append("client_id", import.meta.env.PUBLIC_AUTH_CLIENT_ID);
  payload.append("returnTo", import.meta.env.PUBLIC_HOST_NAME + "/");
  

  return context.redirect(
    "https://" +
    import.meta.env.PUBLIC_AUTH_DOMAIN_URL +
    "/v2/logout?" +
    payload.toString()
  );
}
