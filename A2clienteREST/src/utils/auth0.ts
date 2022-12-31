import type { APIContext } from "astro";
import cookies from "../cookies";
import jwt_decode from "jwt-decode";

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
  id_token: string;
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
  context.cookies.set(cookies.idToken, response.id_token as string, {
    path: "/",
  });
}

export async function getAccessToken(context: APIContext): Promise<string> {
  if (!context.cookies.has(cookies.accessToken)) {
    try {
      const refreshToken = context.cookies.get(cookies.refreshToken)
      .value as string;
      const response = await refreshAccessToken(refreshToken);
      setCookies(context, response);
    } catch (e) {}
  }

  return context.cookies.get(cookies.accessToken).value as string;
}

export async function getIdToken(context: APIContext): Promise<string> {
  return context.cookies.get(cookies.idToken).value as string;
}

export function isLoggedIn(context: APIContext) {
  return context.cookies.has(cookies.refreshToken);
}

export async function getUserId(context: APIContext): Promise<string> {
  const accessToken = await getAccessToken(context);
  if (accessToken) {
    const decoded: any = jwt_decode(accessToken);
    return decoded.sub as string;
  } else {
    return "";
  }
}

export async function getUserEmail(context: APIContext): Promise<string> {
  const idToken = await getIdToken(context);
  if (idToken) {
    const decoded: any = jwt_decode(idToken);
    return decoded.email as string;
  } else {
    return "";
  }
}

// Permissions need to be added to Auth0 API from dashboard (read:users)
export async function getUserEmailById(context: APIContext, userId: string): Promise<string> {
  const accessToken = await getAccessToken(context);
  if (userId && accessToken) {
    const response = await fetch(
      `${import.meta.env.PUBLIC_AUTH0_BASEURL}/api/v2/users/%7B${userId}%7D`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${accessToken}`
        },
      }
    ).then((x) => x.json());
    console.log(response);
    return response.email;
  } else {
    return "";
  }
}