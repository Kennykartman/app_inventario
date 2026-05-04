import smtplib
from email.mime.text import MIMEText

EMAIL = 'jjjjlopez86@gmail.com'
PASSWORD = 'nzpi txtf uniq hxrk'

def enviar_correo(destinatario, asunto, mensaje):

    msg = MIMEText(mensaje)
    msg['Subject'] = asunto
    msg['from'] = EMAIL
    msg['to'] = ','.join(destinatario)

    try:
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(EMAIL,PASSWORD)
        server.sendmail(EMAIL,destinatario,msg.as_string())
        server.quit()
    except Exception as e:
        print('Error correo: ', e)



