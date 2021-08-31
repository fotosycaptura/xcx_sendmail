from flask import Flask, render_template
from flaskext.markdown import Markdown
from classes.cartero import cartero
from classes.datos_csv import datos_csv
import pandas as pd

"""
Sección de configuración

Se define si es testing con True
En producción es False
"""
MODO_TESTING = True


"""
Se define si es modo normal de archivos adjuntos o si es mediante id
MODO_ADJUNTOS = 'NORMAL' si es adjunto normal
MODO_ADJUNTOS = 'VARIABLE' si es diferenciado por id
"""
MODO_ADJUNTOS = 'NORMAL'


"""
Cuenta de correo receptor testing
"""
CORREO_RECEPTOR = ''
CORREO_RECEPTOR_CC = ''

"""
Asunto o Subject
"""
CORREO_ASUNTO_SUBJECT = 'Asunto Testing'


"""
Fin sección de configuración
"""

app = Flask(__name__, template_folder="templates")

Markdown(app)

@app.route('/')
def principal():
    content = ""
    with open("./markdown/contenido.md", "r", encoding="utf-8") as f:
        content = f.read()
    listado_correos = datos_csv.get_rectores()
    return render_template('index.html', contenido=content, listado=listado_correos, funcionando_en_testing=MODO_TESTING, adjuntos=MODO_ADJUNTOS, subject=CORREO_ASUNTO_SUBJECT)

@app.route('/enviar', methods=["POST"])
def enviar():
    content = ""
    with open("./markdown/contenido.md", "r", encoding="utf-8") as f:
        content = f.read()
    rectores = datos_csv.get_rectores()
    log_data = []
    for index, rector in rectores.iterrows():
        #render del texto de correo
        cuerpo = render_template('cuerpo.html', contenido=content)
        #Señor(a)
        cuerpo = cuerpo.replace('{strSenioria}', rector['strSenioria'])
        #Nombre
        cuerpo = cuerpo.replace('{strNombre}', rector['strNombre'])
        #Cargo
        cuerpo = cuerpo.replace('{strCargo}', rector['strCargo'])
        #Institucion
        cuerpo = cuerpo.replace('{strInstitucion}', rector['strInstitucion'])

        if (MODO_TESTING):
            # Listado de recipientes TESTING
            listado_correos = []
            listado_correos.append(CORREO_RECEPTOR)
            listado_correos.append(CORREO_RECEPTOR_CC)

            if (MODO_ADJUNTOS == 'NORMAL'):
                # Enviar correo normal
                rector['Envio'] = cartero.enviar(CORREO_ASUNTO_SUBJECT, listado_correos, cuerpo)
                # Se agregan al log
                log_data.append([rector['id'], rector['strInstitucion'], rector['strEmail'], rector['strEmail02'], rector['Envio']])
                break
            else:
                rector['Envio'] = cartero.enviar_attach_variant(rector['id'], CORREO_ASUNTO_SUBJECT, listado_correos, cuerpo)
                # Se agregan al log
                log_data.append([rector['id'], rector['strInstitucion'], rector['strEmail'], rector['strEmail02'], rector['Envio']])
                break
        else:
            """
            Envío de correos en modo producción
            """
            #Listado de receptores del correo
            listado_correos = []
            listado_correos.append(rector['strEmail'])

            #Si es que hubiera un segundo receptor de correo.
            if len(rector['strEmail02']) > 0:
                listado_correos.append(rector['strEmail02'])

            if MODO_ADJUNTOS == 'NORMAL':
                #Enviar correo normal
                rector['Envio'] = cartero.enviar(CORREO_ASUNTO_SUBJECT, listado_correos, cuerpo)
                # Se agrega al log
                log_data.append([rector['id'], rector['strInstitucion'], rector['strEmail'], rector['strEmail02'], rector['Envio']])
            else:
                rector['Envio'] = cartero.enviar_attach_variant(rector['id'], CORREO_ASUNTO_SUBJECT, listado_correos, cuerpo)
                # Se agrega al log
                log_data.append([rector['id'], rector['strInstitucion'], rector['strEmail'], rector['strEmail02'], rector['Envio']])

    # Para cualquier caso, se guarda el log de los envíos a un csv
    resultado = pd.DataFrame(log_data, columns=['id', 'strInstitucion', 'strEmail', 'strEmail02', 'Envio'])
    resultado.to_csv('rectores_procesados.csv', sep=';', encoding='utf-8-sig', index=False, index_label=None)
    return render_template('procesado.html', funcionando_en_testing=MODO_TESTING, adjuntos=MODO_ADJUNTOS, proceso=resultado)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=8000)
