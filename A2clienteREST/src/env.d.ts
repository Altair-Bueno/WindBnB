/// <reference types="astro/client" />

interface ImportMetaEnv {
  readonly RESERVAS_BASE_PATH: string;
  readonly VIVIENDAS_BASE_PATH: string;
  readonly DATOSABIERTOS_BASE_PATH: string;
  readonly POSITION_STACK_API_KEY: string;
  readonly CLOUDINARY_CLOUD_NAME: string;
  readonly CLOUDINARY_UPLOAD_PRESET: string;
  readonly PUBLIC_PAYPAL_CLIENTID: string;

  readonly AUTH0_CLIENTSECRET: string;
  readonly PUBLIC_AUTH0_CLIENTID: string;
  readonly PUBLIC_AUTH0_BASEURL: string;
  readonly PUBLIC_AUTH0_AUDIENCE: string;
}
