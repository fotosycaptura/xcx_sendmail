# xcx_SENDMAIL

Aplicación para envío de correos masivos personalizados.

## Características

* Utiliza un archivo csv como base de datos donde estarán los listados de correos, junto con sus nombres, cargos, etc.
* Al término del proceso, general un archivo csv donde indica cuales fueron enviados y cuales no.
* Plantilla de correo en formato MarkDown.

## Para instalar los requerimientos simplemente ejecute
```sh
pip install -r requirements.txt
```
## Configuración del servicio de correos

La configuración del servicio de correos se realiza en  la cabecera del archivo classes/cartero.py

## Datos

Los datos se deben de incluir dentro de la carpeta datos/datos.csv, en el formato que se administra la plantilla.
*Nota:* La primera columna sin nombre debe de ser única, pues es un indice para usar de forma interna.

## Adjuntos

Para el envío de archivos adjuntos, se debe de crear dentro de la aplicación la carpeta de nombre *adjuntos*, y dentro de ella, agregar los archivos que se necesiten
adjuntar con el envío de cada correo.

Para el envío de adjuntos diferenciados por id, se debe de crear dentro de la aplicación, la carpeta de nombre *adjuntos-by-id*, y nombrarlos de acuerdo al id del csv.<br/>
**Nota:** 
* Si una institución existe y el archivo no, el correo **NO** se enviará. Lo mismo ocurre si la carpeta no existe.
* Si desea usar esta función, debe especificar su uso en la sección de enviar correos diferenciados por id, definido en *index.py*

# Plantilla de texto para el correo

El texto para colocar en el cuerpo del correo, debe estar incluído en markdown/contenido.md, en formato markdown. Tal como se administra en la plantilla.

Creado con Python 3.9, Flask