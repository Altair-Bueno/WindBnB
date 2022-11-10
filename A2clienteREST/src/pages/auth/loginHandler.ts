import type { APIContext } from "astro";
import Cookies from "../../cookies";

export const FormDataKeys = {
  userid: "userid",
  origin: "origin",
};

export async function post(context: APIContext) {
  const formData = await context.request.formData();

  const userid = formData.get(FormDataKeys.userid);
  const url = formData.get(FormDataKeys.origin) ?? "/";

  if (!userid) {
    throw new Error("Missing userid");
  }

  context.cookies.set(Cookies.USER_ID_KEY, userid.toString(), { path: "/" });

  return context.redirect(url.toString());
}
