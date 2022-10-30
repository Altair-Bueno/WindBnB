from pydantic import BaseModel
from typing import List
from pydantic.fields import Field


class EESSPrecio(BaseModel):
  # Dirección: str
  #  #Horario: str
  latitud: str = Field(alias="Latitud")
  #  #Localidad: str
  longitud: str = Field(alias="Longitud (WGS84)")
  #  #Margen: str
  municipio: str = Field(alias="Municipio")
  #  #Precio_x0020_Biodiesel: str
  #  #Precio_x0020_Bioetanol: str
  #  #Precio_x0020_Gas_x0020_Natural_x0020_Comprimido: str
  #  #Precio_x0020_Gas_x0020_Natural_x0020_Licuado: str
  #  #Precio_x0020_Gases_x0020_licuados_x0020_del_x0020_petróleo: str
  #  #Precio_x0020_Gasoleo_x0020_A: str
  #  #Precio_x0020_Gasoleo_x0020_B: str
  #  #Precio_x0020_Gasoleo_x0020_Premium: str
  #  #Precio_x0020_Gasolina_x0020_95_x0020_E10: str
  #  #Precio_x0020_Gasolina_x0020_95_x0020_E5: str
  #  #Precio_x0020_Gasolina_x0020_95_x0020_E5_x0020_Premium: str
  #  #Precio_x0020_Gasolina_x0020_98_x0020_E10: str
  #  #Precio_x0020_Gasolina_x0020_98_x0020_E5: str
  #  #Precio_x0020_Hidrogeno: str
  provincia: str = Field(alias="Provincia")
  #  #Remisión: str
  #  #Rótulo: str
  #  #Tipo_x0020_Venta: str
  #  #_x0025__x0020_BioEtanol: str
  #  #_x0025__x0020_Éster_x0020_metílico: str
  #  #IDEESS: str
  #  #IDMunicipio: str
  #  #IDProvincia: str
  #  #IDCCAA: str


class GasStation(BaseModel):
  Fecha: str
  ListaEESSPrecio: List[EESSPrecio] = []
  Nota: str
  ResultadoConsulta: str
