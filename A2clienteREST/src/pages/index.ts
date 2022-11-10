import type { APIContext } from "astro";

/**
 * Redirects the / route to `/houses` (list of houses)
 */
export async function get(context: APIContext) {
  return context.redirect("/houses");
}
