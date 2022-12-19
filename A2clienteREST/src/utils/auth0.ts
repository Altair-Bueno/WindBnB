import type { APIContext } from "astro";
import cookies from "../cookies";

// https://auth0.com/docs/api/authentication#refresh-token
async function refreshAccessToken(refresh_token: string) {
  const payload = new URLSearchParams({
    grant_type: "refresh_token",
    client_id: import.meta.env.PUBLIC_AUTH0_CLIENTID,
    client_secret: import.meta.env.AUTH0_CLIENTSECRET,
    refresh_token,
  });

  const response = await fetch(
    `${import.meta.env.PUBLIC_AUTH0_BASEURL}/oauth/token`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: payload.toString(),
    }
  ).then((x) => x.json());
  return response;
}
interface TokenPayload {
  access_token: string;
  refresh_token: string;
  scope: string;
  expires_in: number;
  token_type: string;
}
export function setCookies(context: APIContext, response: TokenPayload) {
  context.cookies.set(cookies.accessToken, response.access_token as string, {
    path: "/",
    expires: new Date(Date.now() + response.expires_in),
  });
  context.cookies.set(cookies.refreshToken, response.refresh_token as string, {
    path: "/",
  });
}

export async function getAccessToken(context: APIContext): Promise<string> {
  if (!context.cookies.has(cookies.accessToken)) {
    const refreshToken = context.cookies.get(cookies.refreshToken)
      .value as string;
    const response = await refreshAccessToken(refreshToken);
    setCookies(context, response);
  }

  return context.cookies.get(cookies.accessToken).value as string;
}

export function isLoggedIn(context: APIContext) {
  return context.cookies.has(cookies.refreshToken);
}
