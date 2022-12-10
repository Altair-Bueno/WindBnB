import type { APIContext } from "astro";
import {createAuth0Client} from '@auth0/auth0-spa-js';

export const URI = "/auth/loginHandler";

export const FormDataKeys = {
  userid: "userid",
  origin: "origin",
};

async function createClient() {
	let auth0Client = await createAuth0Client({
		domain: "dev-b24klp0bqjdg0iaq.us.auth0.com",
		clientId: "wt7qbwCEMdjbZQIkDgYHurw7adhhjoWf"
	});
	return auth0Client;
}

async function loginWithPopup(client, options) {
	//popupOpen.set(true);
	try {
		await client.loginWithPopup(options);

		//user.set(await client.getUser());
		//isAuthenticated.set(true);
	} catch (e) {
		// eslint-disable-next-line
		console.error(e);
	} finally {
		//popupOpen.set(false);
	}
}

function logout(client) {
	return client.logout();
}


export async function post(context: APIContext) {
  console.log("loginHandler");
  /*
  const formData = await context.request.formData();

  const userid = formData.get(FormDataKeys.userid);
  const url = formData.get(FormDataKeys.origin) ?? "/";

  if (!userid) {
    return context.redirect("/");
  }

  context.cookies.set(Cookies.USER_ID_KEY, userid.toString(), { path: "/" });
  return context.redirect(url.toString());
  */

  let auth0Client = await createClient();
  await loginWithPopup(auth0Client, {});

}
