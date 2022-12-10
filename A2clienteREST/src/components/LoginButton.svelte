<script>
import {createAuth0Client} from '@auth0/auth0-spa-js';
import "../styles/bootstrap.scss";

// Crea una nueva instancia del cliente Auth0
const auth0 = createAuth0Client({
    domain: "dev-b24klp0bqjdg0iaq.us.auth0.com",
	clientId: "wt7qbwCEMdjbZQIkDgYHurw7adhhjoWf"
});

// Inicia el flujo de inicio de sesión
async function login() {
  await (await auth0).loginWithRedirect(
    {
      redirect_uri: "http://localhost:3000"
    }
  );
  await auth0.handleRedirectCallback();
}

// Obtiene información del usuario autenticado
async function getUser() {
  const user = await auth0.getUser();
  console.log(user);
}
</script>

<button class="btn btn-primary" on:click={login}>Iniciar sesión</button>
