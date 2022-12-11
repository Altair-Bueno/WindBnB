/// <reference types="astro/client" />

interface ImportMetaEnv {
  readonly RESERVAS_BASE_PATH: string;
  readonly VIVIENDAS_BASE_PATH: string;
  readonly DATOSABIERTOS_BASE_PATH: string;
  readonly POSITION_STACK_API_KEY: string;
  readonly CLOUDINARY_CLOUD_NAME: string;
  readonly CLOUDINARY_UPLOAD_PRESET: string;
  readonly PUBLIC_PAYPAL_CLIENTID: string;
  readonly PUBLIC_AUTH_DOMAIN_URL: string;
  readonly PUBLIC_AUTH_REDIRECT_URL: string;
  readonly PUBLIC_AUTH_CLIENT_ID: string;
  readonly AUTH_CLIENT_SECRET: string;
  readonly PUBLIC_HOST_NAME: string;
}
