import type { APIContext } from "astro";
import Cookies from "../../cookies";

export const FormDataKeys = {
  origin: "origin",
};

export async function post(context: APIContext) {
  context.cookies.delete(Cookies.USER_ID_KEY, { path: "/" });
  const url = await context.request
    .formData()
    .then((x) => x.get(FormDataKeys.origin));
  return context.redirect(url?.toString() ?? "/");
}
