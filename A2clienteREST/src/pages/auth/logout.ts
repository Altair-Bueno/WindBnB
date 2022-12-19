import type { APIContext } from "astro";
import cookies from "../../cookies";

export async function post(context: APIContext) {
  context.cookies.delete(cookies.accessToken, { path: "/" });
  context.cookies.delete(cookies.refreshToken, { path: "/" });

  // https://auth0.com/docs/api/authentication#logout
  const payload = new URLSearchParams({
    client_id: import.meta.env.PUBLIC_AUTH0_CLIENTID,
    returnTo: context.url.origin,
  });
  return context.redirect(
    `${import.meta.env.PUBLIC_AUTH0_BASEURL}/v2/logout?${payload}`
  );
}
