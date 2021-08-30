from flask import Flask, render_template
from flaskext.markdown import Markdown
from classes.cartero import cartero
from classes.datos_csv import datos_csv
import pandas as pd

app = Flask(__name__, template_folder="templates")

Markdown(app)

@app.route('/')
def principal():
    content = ""
    with open("./markdown/contenido.md", "r", encoding="utf-8") as f:
        content = f.read()
    listado_correos = datos_csv.get_rectores()
    return render_template('index.html', contenido=content, listado=listado_correos)

@app.route('/enviar', methods=["POST"])
def enviar():
    content = ""
    with open("./markdown/contenido.md", "r", encoding="utf-8") as f:
        content = f.read()
    cuerpo = render_template('cuerpo.html', contenido=content)
    rectores = datos_csv.get_rectores()
    data = []
    for index, rector in rectores.iterrows():
        #Señor(a)
        cuerpo = cuerpo.replace('{strSenioria}', rector['strSenioria'])
        #Nombre
        cuerpo = cuerpo.replace('{strNombre}', rector['strNombre'])
        #Cargo
        cuerpo = cuerpo.replace('{strCargo}', rector['strCargo'])
        #Institucion
        cuerpo = cuerpo.replace('{strInstitucion}', rector['strInstitucion'])

        #Listado de receptores del correo
        listado_correos = []
        listado_correos.append(rector['strEmail'])

        #Si es que hubiera un segundo receptor de correo.
        if len(rector['strEmail02']) > 0:
            listado_correos.append(rector['strEmail02'])

        #Enviado desde el cartero
        rector['Envio'] = cartero.enviar('Asunto de prueba', listado_correos, cuerpo)
        data.append([rector['id'], rector['strInstitucion'], rector['strEmail'], rector['strEmail02'], rector['Envio']])

    resultado = pd.DataFrame(data, columns=['id', 'strInstitucion', 'strEmail', 'strEmail02', 'Envio'])
    resultado.to_csv('rectores_procesados.csv', sep=';', encoding='utf-8-sig', index=False, index_label=None)
    return render_template('procesado.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=8000)
