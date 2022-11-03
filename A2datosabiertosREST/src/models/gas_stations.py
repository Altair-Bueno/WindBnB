from pydantic import BaseModel
from typing import List, Optional
from pydantic.fields import Field


class EESSPrecio(BaseModel):
    cp: str = Field(alias="C.P.")
    direccion: str = Field(alias="Dirección")
    horario: str = Field(alias="Horario")
    latitud: str = Field(alias="Latitud")
    localidad: str = Field(alias="Localidad")
    longitud: str = Field(alias="Longitud (WGS84)")
    #  #Margen: str
    municipio: str = Field(alias="Municipio")
    biodiesel: str = Field(alias="Precio Biodiesel")
    bioetanol: str = Field(alias="Precio Bioetanol")
    gas_natural_comprimido: str = Field(alias="Precio Gas Natural Comprimido")
    gas_natural_licudado: str = Field(alias="Precio Gas Natural Licuado")
    gases_licuados_del_petroleo: str = Field(alias="Precio Gases licuados del petróleo")
    gasoleo_a: str = Field(alias="Precio Gasoleo A")
    gasoleo_b: str = Field(alias="Precio Gasoleo B")
    gasoleo_premium: str = Field(alias="Precio Gasoleo Premium")
    gasolina_95_e10: str = Field(alias="Precio Gasolina 95 E10")
    gasolina_95_e5: str = Field(alias="Precio Gasolina 95 E5")
    gasolina_95_e5_premium: str = Field(alias="Precio Gasolina 95 E5 Premium")
    gasolina_98_e10: str = Field(alias="Precio Gasolina 98 E10")
    gasolina_98_e5: str = Field(alias="Precio Gasolina 98 E5")
    hidrogeno: str = Field(alias="Precio Hidrogeno")
    provincia: str = Field(alias="Provincia")
    #  #Remisión: str
    rotulo: str = Field(alias="Rótulo")
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


class EESSPrecioFilter(BaseModel):
    provincia: Optional[str]
    rotulo: Optional[str]
