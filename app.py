from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pytz

app = Flask(__name__)

# Configuración del servidor SMTP y credenciales
SMTP_SERVER = "smtp.upch.pe"
SMTP_PORT = 587
SMTP_USERNAME = "yojan.manosalva@upch.pe"
SMTP_PASSWORD = "contraseña"  # ¡Recuerda reemplazar con tu contraseña real!

# Zona horaria de Perú
PERU_TZ = pytz.timezone('America/Lima')

# Diccionario para almacenar cursos y sus entregables
courses = {
    'curso1': {
        'name': 'Datos y Redes',
        'image': 'curso1.jpg',
        'deliverables': []
    },
    'curso2': {
        'name': 'Química Computacional',
        'image': 'curso2.jpg',
        'deliverables': []
    },
    'curso3': {
        'name': 'Proyectos de Software',
        'image': 'curso3.jpg',
        'deliverables': []
    },
    'curso4': {
        'name': 'Machine Learning',
        'image': 'curso4.jpg',
        'deliverables': []
    },
    'curso5': {
        'name': 'Sistemas Operativos',
        'image': 'curso5.jpg',
        'deliverables': []
    }
}

# Función para enviar un correo electrónico
def send_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = SMTP_USERNAME
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)

        server.sendmail(SMTP_USERNAME, SMTP_USERNAME, msg.as_string())
        server.quit()
        print("Correo electrónico enviado correctamente.")
    except Exception as e:
        print("Error al enviar el correo electrónico:", str(e))

# Ruta para la página de inicio
@app.route('/')
def index():
    return render_template('index.html', courses=courses)

# Ruta para la página de detalles de cada curso
@app.route('/course/<course_name>', methods=['GET', 'POST'])
def course(course_name):
    course_name = course_name.lower()
    if course_name in courses:
        if request.method == 'POST':
            deliverable_name = request.form['deliverable_name']
            deadline_date = request.form['deadline_date']
            deadline_time = request.form['deadline_time']
            deadline = datetime.strptime(deadline_date + ' ' + deadline_time, '%Y-%m-%d %H:%M')
            courses[course_name]['deliverables'].append({'name': deliverable_name, 'deadline': deadline})
            # Ordenar los entregables por fecha de vencimiento
            courses[course_name]['deliverables'] = sorted(courses[course_name]['deliverables'], key=lambda x: x['deadline'])
            # Convertir la fecha de entrega a la zona horaria de Perú
            deadline_peru = deadline.astimezone(PERU_TZ)
            # Enviar correo electrónico de alerta si la fecha de entrega es en menos de 24 horas
            if deadline_peru - datetime.now(PERU_TZ) <= timedelta(days=1):
                subject = f"Entrega próxima para el curso {courses[course_name]['name']}"
                body = f"Recuerda que tienes una entrega próxima para el curso {courses[course_name]['name']} el {deadline_peru}. ¡No te olvides!"
                send_email(subject, body)
            return redirect(url_for('course', course_name=course_name))
        return render_template('course.html', course_name=course_name, course=courses[course_name])
    else:
        return "El curso no existe."

if __name__ == '__main__':
    app.run(debug=True)
