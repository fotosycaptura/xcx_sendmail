#!/usr/bin/env python3
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import os
from os.path import basename
from pathlib import Path

""" Configuración de cuenta de correo """
password = ''
remitente = ''
host_servicio = ''
host_puerto = 587

""" Configuración de carpetas de adjuntos """
adjuntos_folder = os.path.abspath("./adjuntos")
adjuntos_variables = os.path.abspath("./adjuntos-by-id")
class cartero():
    """ 
    Envía un correo, con o sin archivo adjunto 
    """
    def enviar(subject, lista_direcciones, cuerpo_del_mensaje):
        global adjuntos_folder

        try:
            # Crea una instancia del objeto mensaje
            msg = MIMEMultipart()
            mensaje = cuerpo_del_mensaje
            # se setean clave y dirección de quien proviene el email 

            global password
            global remitente
            global host_servicio
            global host_puerto

            msg['From'] = remitente

            # Se setean parámetros del correo, subject, direccion
            msg['To'] = ", ".join(lista_direcciones)
            msg['Subject'] = subject

            # añade en el cuerpo del mensaje del email
            msg.attach(MIMEText(mensaje, 'html'))

            server = smtplib.SMTP(host = host_servicio, port = host_puerto)
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
            # Envía email
            server.sendmail(msg['From'], lista_direcciones, msg.as_string())
            server.quit()

            # En algunos servicios de correos, si se envian dos o más segundos de cierto tiempo, se bloquean por spam
            time.sleep(1)
            return 'OK'
        except:
            return 'No'

    """ 
    Envía un correo siempre que exista el archivo asociado al id, de lo contrario no envía el correo 
    """
    def enviar_attach_variant(id_rector, subject, lista_direcciones, cuerpo_del_mensaje):
        global adjuntos_variables
        try:
            # Crea una instancia del objeto mensaje
            msg = MIMEMultipart()
            mensaje = cuerpo_del_mensaje

            # Para acceder a las variables definidas al comienzo como globales
            global password
            global remitente
            global host_servicio
            global host_puerto

            msg['From'] = remitente

            # Se setean parámetros del correo, subject, direccion
            msg['To'] = ", ".join(lista_direcciones)
            msg['Subject'] = subject

            # añade en el cuerpo del mensaje del email
            msg.attach(MIMEText(mensaje, 'html'))

            server = smtplib.SMTP(host = host_servicio, port = host_puerto)
            server.starttls()
            # Logueo con credenciales 
            server.login(msg['From'], password)

            # Se verifica la existencia de la carpeta de archivos
            if os.path.exists(os.path.join(adjuntos_variables)):
                bl_Encontrado = False
                # Se recorre el contenido de la carpeta 
                for root, dirs, files in os.walk(adjuntos_variables):
                    for names in files:
                        filepath = os.path.join(root, names)
                        file_name = Path(filepath).stem
                        if (file_name == str(id_rector)):
                            with open(filepath, "rb") as fil:
                                part = MIMEApplication(
                                    fil.read(),
                                    Name=basename(filepath)
                                )
                                # After the file is closed
                                part['Content-Disposition'] = 'attachment; filename="%s"' % basename(filepath)
                            msg.attach(part)
                            bl_Encontrado = True
                # Envía email
                if (bl_Encontrado):
                    server.sendmail(msg['From'], lista_direcciones, msg.as_string())
                    server.quit()
                    time.sleep(1)
                    return 'OK'
                else:
                    return 'No archivos'
            else:
                return 'No hay carpeta de adjuntos variables.'
        except:
            return 'No'