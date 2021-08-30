#!/usr/bin/env python3
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import os
from os.path import basename
class cartero():
    def enviar(subject, lista_direcciones, cuerpoDelMensaje):

        # Configuraciones para adjuntos y cuenta de correo.
        adjuntos_folder = os.path.abspath("./adjuntos")
        cuenta_correo = ''
        clave_correo = ''
        host_correo = '' 
        puerto_correo = 587

        try:
            # Crea una instancia del objeto mensaje
            msg = MIMEMultipart()
            mensaje = cuerpoDelMensaje
            # se setean clave y dirección de quien proviene el email 
            password = clave_correo
            msg['From'] = cuenta_correo

            # Se setean parámetros del correo, subject, direccion
            msg['To'] = ", ".join(lista_direcciones)
            msg['Subject'] = subject

            # añade en el cuerpo del mensaje del email
            msg.attach(MIMEText(mensaje, 'html'))

            server = smtplib.SMTP(host = host_correo, port = puerto_correo)
            server.starttls()
            # Logueo con credenciales 
            server.login(msg['From'], password)

            # Adjuntos de archivos, si es que hay
            if os.path.exists(os.path.join(adjuntos_folder)):
                for root, dirs, files in os.walk(adjuntos_folder):
                    for names in files:
                        filepath = os.path.join(root, names)
                        
                        with open(filepath, "rb") as fil:
                            part = MIMEApplication(
                                fil.read(),
                                Name=basename(filepath)
                            )
                            # After the file is closed
                            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(filepath)
                        msg.attach(part)
            else:
                print('No hay archivos para adjuntar o no se encuentra la carpeta')

            # Envía email
            server.sendmail(msg['From'], lista_direcciones, msg.as_string())
            server.quit()

            # En algunos servicios de correos, si se envian dos o más segundos de cierto tiempo, se bloquean por spam
            time.sleep(1)
            return 'OK'
        except:
            return 'No'

