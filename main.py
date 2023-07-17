from flask import Flask, jsonify,render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re #modificacion de cadenas
######################################
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
import io #entrada y salida de memoria
import base64 #datos binarios
from datetime import datetime
#pip install flask-mysqldb

app = Flask(__name__)
app.secret_key = '1a2b3c4d5e'
# detalles de conexión a la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '71396417'
app.config['MYSQL_DB'] = 'voluntario'

# Inicializar MySQL
mysql = MySQL(app)


###########################################################
import smtplib
from email.message import EmailMessage
def enviarCorreo(archivoMsje):
    emisor="emilyjhas@gmail.com"
    receptor="emilyjhas@gmail.com"
    
    with open(archivoMsje) as fp:
        msge = EmailMessage()
        msge.set_content(fp.read())
    
    msge['Subject'] = f'Mensaje importante: {archivoMsje}'
    msge['From'] = emisor
    msge['To'] = receptor
    
    s = smtplib.SMTP('localhost')
    s.send_message(msge)
    s.quit()
###########################################################


# http://localhost:5000/diagnosticoVoluntariado/ - esta será la página de inicio de sesión
@app.route('/', methods=['GET', 'POST']) #especificacion de la url de la funcion
def primeraPantalla():
    return render_template('intro.html')

@app.route('/diagnosticoVoluntariado/', methods=['GET', 'POST'])
def login():
    msg = '' #almacenar mensajes
    # Verificamos si existen solicitudes POST de "nombre de usuario" y "contraseña" (formulario enviado por el usuario)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Verifique si la cuenta existe
        print ("username: ",username)
        print ("password",password )
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) #acceso a los datos
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone() #se obtiene
        # Si la cuenta existe en la base de datos
        if account:
            # Creamos datos de sesión, podemos acceder a estos datos en otras rutas
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            #session['pre_test'] = account['pre_test']
            #session['post_test'] = account['post_test']   
            session['tipo_usuario'] = account['tipo_usuario']
            #session['aceptacion_terminos'] = account['aceptacion_terminos']            
               
            # Redirigir a la página de inicio
            if account['tipo_usuario']  == 0:
                #return redirect(url_for('home'))
                msg = 'Solo los administradores pueden acceder al sistema'
            else:
                return redirect(url_for('resultados'))                
        else:
            # La cuenta no existe o el nombre de usuario / contraseña es incorrecto
            msg = 'Usuario o password incorrectos!'
    return render_template('index.html', msg=msg)


def grafico_variable_fuzzy(fig,rutaImagen):
    img = io.BytesIO()
    fig.savefig(rutaImagen) 
    img.seek(0) #puntero datos
    graph_url = base64.b64encode(img.getvalue()).decode()

    return 'data:image/png;base64,{}'.format(graph_url)

def ParteDifusa(VADIDF):
        
    valoresP = ctrl.Antecedent(np.linspace(0, 20, 5), 'valoresP') 
    capacidadesP = ctrl.Antecedent(np.linspace(0, 42, 7), 'capacidadesP')
    proactividadP = ctrl.Antecedent(np.linspace(0, 40, 10), 'proactividadP')
    
    nivelVoluntariado = ctrl.Consequent(np.linspace(0, 99, 9), 'nivelVoluntariado')
    
    valoresP['minima'] = fuzz.trapmf(valoresP.universe, [0,0,4.92, 9.65 ])
    valoresP['moderada'] = fuzz.trimf(valoresP.universe, [4.92,  9.65 ,14.57])
    valoresP['elevada'] = fuzz.trapmf(valoresP.universe, [9.65,14.57,20,20])
     
    capacidadesP['minima'] = fuzz.trapmf(capacidadesP.universe, [0, 0, 18.92, 21.91])
    capacidadesP['moderada'] = fuzz.trimf(capacidadesP.universe, [18.92,21.91 ,24.9])
    capacidadesP['elevada'] = fuzz.trapmf(capacidadesP.universe, [21.91,24.9,42,42])
    
    proactividadP['minima'] = fuzz.trapmf(proactividadP.universe, [0, 0, 18.92 , 21.91])
    proactividadP['moderada'] = fuzz.trimf(proactividadP.universe, [18.92,21.91 ,24.9])    
    proactividadP['elevada'] = fuzz.trapmf(proactividadP.universe, [21.91,24.9,40,40])    
            
    # #Variable linguistica de salida
    nivelVoluntariado['Baja'] = fuzz.trapmf(nivelVoluntariado.universe, [0,0, 25, 50])
    nivelVoluntariado['Media'] = fuzz.trimf(nivelVoluntariado.universe, [25, 50, 75])
    nivelVoluntariado['Alta'] = fuzz.trapmf(nivelVoluntariado.universe, [50, 75,99,99])
    
#################################################################################################
    figEntrada1 =ctrl.fuzzyvariable.FuzzyVariableVisualizer(valoresP).view() 
    figEntrada2 =ctrl.fuzzyvariable.FuzzyVariableVisualizer(capacidadesP).view()       
    figEntrada3 =ctrl.fuzzyvariable.FuzzyVariableVisualizer(proactividadP).view()
    figNCG =ctrl.fuzzyvariable.FuzzyVariableVisualizer(nivelVoluntariado).view() 
    graph1_url = grafico_variable_fuzzy(figEntrada1[0],"static/images/fuzzy/valoresP.jpg")    
    graph2_url = grafico_variable_fuzzy(figEntrada2[0],"static/images/fuzzy/capacidadesP.jpg")
    graph3_url = grafico_variable_fuzzy(figEntrada3[0],"static/images/fuzzy/proactividadP.jpg")
    graph6_url = grafico_variable_fuzzy(figNCG[0],"static/images/fuzzy/nivelVoluntariado.jpg")
    
#################################################################################################
    
    #-------reglas nivelVoluntariado
    rule1 = ctrl.Rule(valoresP['minima'] & capacidadesP['minima'] & proactividadP['minima'] , nivelVoluntariado['Baja'])
    rule2 = ctrl.Rule(valoresP['minima'] & capacidadesP['minima'] & proactividadP['moderada'] , nivelVoluntariado['Baja'])
    rule3 = ctrl.Rule(valoresP['minima'] & capacidadesP['minima'] & proactividadP['elevada'] , nivelVoluntariado['Media'])
    rule4 = ctrl.Rule(valoresP['minima'] & capacidadesP['moderada'] & proactividadP['minima'] , nivelVoluntariado['Baja'])        
    rule5 = ctrl.Rule(valoresP['minima'] & capacidadesP['moderada'] & proactividadP['moderada']   , nivelVoluntariado['Media'])
    rule6 = ctrl.Rule(valoresP['minima'] & capacidadesP['moderada'] & proactividadP['elevada']   , nivelVoluntariado['Alta'])
    rule7 = ctrl.Rule(valoresP['minima'] & capacidadesP['elevada'] & proactividadP['minima']   , nivelVoluntariado['Media'])
    rule8 = ctrl.Rule(valoresP['minima'] & capacidadesP['elevada'] & proactividadP['moderada']   , nivelVoluntariado['Media'])                
    rule9 =  ctrl.Rule(valoresP['minima'] & capacidadesP['elevada'] & proactividadP['elevada']  , nivelVoluntariado['Alta'])

    rule10 = ctrl.Rule(valoresP['moderada'] & capacidadesP['minima'] & proactividadP['minima']  , nivelVoluntariado['Baja'])
    rule11 = ctrl.Rule(valoresP['moderada'] & capacidadesP['minima'] & proactividadP['moderada']  , nivelVoluntariado['Baja']) 
    rule12 = ctrl.Rule(valoresP['moderada'] & capacidadesP['minima'] & proactividadP['elevada']  , nivelVoluntariado['Media'])        
    rule13 = ctrl.Rule(valoresP['moderada'] & capacidadesP['moderada'] & proactividadP['minima']    , nivelVoluntariado['Media'])
    rule14 = ctrl.Rule(valoresP['moderada'] & capacidadesP['moderada'] & proactividadP['moderada']    , nivelVoluntariado['Media'])
    rule15 = ctrl.Rule(valoresP['moderada'] & capacidadesP['moderada'] & proactividadP['elevada']    , nivelVoluntariado['Media'])
    rule16 = ctrl.Rule(valoresP['moderada'] & capacidadesP['elevada'] & proactividadP['minima']    , nivelVoluntariado['Media'])        
    rule17 = ctrl.Rule(valoresP['moderada'] & capacidadesP['elevada'] & proactividadP['moderada']  , nivelVoluntariado['Media'])
    rule18 = ctrl.Rule(valoresP['moderada'] & capacidadesP['elevada'] & proactividadP['elevada']  , nivelVoluntariado['Alta'])

    rule19 = ctrl.Rule(valoresP['elevada'] & capacidadesP['minima'] & proactividadP['minima']  , nivelVoluntariado['Baja'])
    rule20 = ctrl.Rule(valoresP['elevada'] & capacidadesP['minima'] & proactividadP['moderada']  , nivelVoluntariado['Media'])        
    rule21 = ctrl.Rule(valoresP['elevada'] & capacidadesP['minima'] & proactividadP['elevada']    , nivelVoluntariado['Media'])
    rule22 = ctrl.Rule(valoresP['elevada'] & capacidadesP['moderada'] & proactividadP['minima']    , nivelVoluntariado['Media'])
    rule23 = ctrl.Rule(valoresP['elevada'] & capacidadesP['moderada'] & proactividadP['moderada']    , nivelVoluntariado['Media'])
    rule24 = ctrl.Rule(valoresP['elevada'] & capacidadesP['moderada'] & proactividadP['elevada']    , nivelVoluntariado['Alta'])                
    rule25 =  ctrl.Rule(valoresP['elevada'] & capacidadesP['elevada'] & proactividadP['minima']   , nivelVoluntariado['Media'])
    rule26 = ctrl.Rule(valoresP['elevada'] & capacidadesP['elevada'] & proactividadP['moderada']    , nivelVoluntariado['Media'])
    rule27 = ctrl.Rule(valoresP['elevada'] & capacidadesP['elevada'] & proactividadP['elevada']    , nivelVoluntariado['Alta'])
    

    acc_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10,rule11, 
                                    rule12, rule13, rule14, rule15, rule16,rule17, rule18, rule19, rule20, rule21,
                                    rule22, rule23, rule24, rule25, rule26,rule27])
    
    acc = ctrl.ControlSystemSimulation(acc_ctrl)
        
    #entradas al sistema
    acc.input['valoresP'] = VADIDF[0]
    acc.input['capacidadesP'] = VADIDF[1]
    acc.input['proactividadP'] = VADIDF[2]   
    acc.compute()
    nivel_diagnostico = acc.output['nivelVoluntariado']
    print("nivel de diagnostico voluntariado: ",nivel_diagnostico)  
   
    figNCG2 =ctrl.fuzzyvariable.FuzzyVariableVisualizer(nivelVoluntariado).view(sim=acc)    
    graph7_url = grafico_variable_fuzzy(figNCG2[0],"static/images/fuzzy/nivelDiagnosticoDefuzz.jpg")        
    return nivel_diagnostico


@app.route('/terminos_condiciones/<int:id_usuario>')
def terminos_condiciones(id_usuario):
    if 'loggedin' in session:
        id_logged=id_usuario       
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE accounts SET aceptacion_terminos = %s WHERE id = %s', (1,id_logged))      
        mysql.connection.commit()
        msg="El postulante ya está habilitado para pasar el test. :)"
    return jsonify(result=msg)    
    

@app.route('/contratar/<int:id_usuario>/<int:band>')
def contratar(id_usuario,band):
    if 'loggedin' in session:
        id_logged=id_usuario       
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE accounts SET aceptado = %s WHERE id = %s', (band,id_logged))      
        mysql.connection.commit()
        #if (band==1):
            #enviarCorreo("aceptar_voluntario.txt")
        #else:
            #enviarCorreo("retirar_voluntario.txt")            
        return redirect(url_for('profile',id_usuario=id_usuario))
    return redirect(url_for('login'))         
######################################################################    
@app.route('/post_diagnostico/<int:id_usuario>')
def post_diagnostico(id_usuario):

    if 'loggedin' in session:    
        respuestas =        [0,0,2,2,1,0,1,0,0,1]   # puntos completos     
        medias_respuestas = [1,1,1,0,0,1,2,1,2,2]   #puntos a la mitad
        VADIDF = [0,0,0] 
        PTOS_MAX = [10,14,8]
        selections = request.args.get('selections')
        selections=selections.strip('[]')
        res = selections.split(',')
        i=0
        print ("marcaciones en la vista html:",res) 
        for elem in res: 
            #print(respuestas[i] ," - ", elem)
            if i<2: #2 items
                pos= 0
                ptos_ = PTOS_MAX [0]
            elif i<5: #3 items
                pos= 1
                ptos_ = PTOS_MAX[1]
            else: #5 items
                pos= 2                
                ptos_ = PTOS_MAX[2]
                
            if respuestas[i] == int(elem):
                VADIDF[pos]+= ptos_
            else:
                if medias_respuestas[i] == int(elem):
                    VADIDF[pos]+= ptos_/2
                else:
                    VADIDF[pos]+=ptos_/4            
            i=i+1
        
        print ("VADIDF: ",VADIDF) 

        nivel_diagnostico = ParteDifusa(VADIDF)
        nivel_diagnostico = round(nivel_diagnostico,2)

        if(nivel_diagnostico>=0 and nivel_diagnostico<=25):
            msg= '<h4>Nivel de aptitud para ser voluntario:</h4> <strong><h3>Baja</h3></strong>'
        elif(nivel_diagnostico>25 and nivel_diagnostico<=60):
            msg= '<h4>Nivel de aptitud para ser voluntario:</h4> <strong><h3>Media</h3></strong>'        
        else:
            msg= '<h4>Nivel de aptitud para ser voluntario:</h4> <strong><h3>Alta</h3></strong>'              
        # msg+= ' -->Y posee un puntaje en el test de: '+ str(nivel_diagnostico)        
        msg+='<br><a style="border: 4px solid green; background-color: green;color: white;padding: 0.3em 1.3em;text-decoration: none;" id="link_pretest" href="/diagnosticoVoluntariado/resultados" class="btn btn-primary">Listo</a>'
        #msg+='<br><br><iframe width="560" height="315" src="https://www.youtube.com/embed/i20dhMXfc4s" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>'
                
        id_logged=id_usuario
        post_test=(nivel_diagnostico)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE accounts SET post_test = %s WHERE id = %s', (post_test, id_logged))      
        mysql.connection.commit()
        return jsonify(result=msg)
    return redirect(url_for('login'))   


#######################################################################


# esta será la página de inicio, solo accesible para usuarios registrados
@app.route('/diagnosticoVoluntariado/home/<int:id_usuario>')
def home(id_usuario):
    # Comprueba si el usuario está conectado
    if 'loggedin' in session:
        # El usuario ha iniciado sesión, mostrarle la página de inicio
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (id_usuario,))
        account = cursor.fetchone()
        print (account)
        
        return render_template('home.html', account=account, aceptacion_terminos=account['aceptacion_terminos'],username=account['username'], pre_test=account['pre_test'], post_test=account['post_test'])
    # El usuario no ha iniciado sesión, redirigir a la página de inicio de sesión
    return redirect(url_for('login'))    

@app.route('/diagnosticoVoluntariado/profile/<int:id_usuario>')
def profile(id_usuario):
    # Compruebe si el usuario está conectado
    if 'loggedin' in session:
        print("id_usuario: ",id_usuario)
        # Necesitamos toda la información de la cuenta del usuario para poder mostrarla en la página de perfil.
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (id_usuario,))
        account = cursor.fetchone()
        # Mostrar la pagina de perfil con informacion de la cuenta
        return render_template('profile.html', aceptacion_terminos=account['aceptacion_terminos'], account=account,username=account['username'])
    # El usuario no ha iniciado sesión, redirigir a la página de inicio de sesión
    return redirect(url_for('login'))

@app.route('/diagnosticoVoluntariado/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('id', None)
    session.pop('username', None)
    #session.pop('pre_test', None)
    #session.pop('post_test', None)    
    session.pop('tipo_usuario', None) 
    
    print("Te desconectaste con exito!!")
    return redirect(url_for('login'))


@app.route('/diagnosticoVoluntariado/quiz_pos/<int:id_usuario>')
def quiz_pos(id_usuario):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (id_usuario,))
        account = cursor.fetchone()
        post_test=account['post_test']
        post_test=int(post_test)
        pre_test=account['pre_test']
        pre_test=int(pre_test) 
        aceptacion_terminos=account['aceptacion_terminos']        
        
        if post_test == -1 and aceptacion_terminos == 1:            
            return render_template('quiz_pos.html', account=account,username=account['username'])
        else:
            return redirect(url_for('home',id_usuario=account['id']))
    return redirect(url_for('login'))

@app.route('/diagnosticoVoluntariado/resultados')
def resultados():
    
    if 'loggedin' in session:
        if session['tipo_usuario'] == 1:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE tipo_usuario = 0 order by post_test desc')
            ListaCuentas = cursor.fetchall()
            print (ListaCuentas)
            
            return render_template('resultados.html',username=session['username'],ListaCuentas=ListaCuentas)    
        else:
            return redirect(url_for('home'))            
    return redirect(url_for('login'))

@app.route('/diagnosticoVoluntariado/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        correo = request.form['correo']
        dni = request.form['dni']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = request.form['edad']
        sexo = request.form['sexo']
        universidad = request.form['universidad']
        carrera = request.form['carrera']
        ciclo = request.form['ciclo']
        tipo_usuario = request.form['tipo_usuario']
        cargo = request.form['cargo']
        password = request.form['password']
        pre_test = int(50) #VALOR POR DEFECTO, PUEDE SER CAMBIADO A CONVENIENCIA
        post_test = int(-1)
        aceptacion_terminos = int(0)
        aceptado = int(0)
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Verificamos si la cuenta existe usando MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # Si la cuenta existe, mostrar errores y verificaciones de validación
        if account:
            msg = 'la cuenta ya existe!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'El nombre de usuario debe contener solo caracteres y números!'
        elif not username or not password:
            msg = 'Porfavor completa el formulario!'
        else:
            # La cuenta no existe y los datos del formulario son válidos, ahora insertamos una nueva cuenta en la tabla accounts
            cursor.execute('INSERT INTO accounts VALUES (NULL,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', [username, correo, dni, nombre, apellido,edad,sexo,universidad,carrera,ciclo,tipo_usuario,cargo,password,pre_test,post_test,aceptacion_terminos,aceptado,date])
#,username,correo,dni,nombre,apellido,edad,sexo,universidad,carrera,ciclo,tipo_usuario,cargo,password,pre_test,post_test,aceptacion_terminos,aceptado,date            
            mysql.connection.commit()
            msg = 'Se ha registrado exitosamente!'
    elif request.method == 'POST':
        # El formulario está vacío ... (no hay datos POST)
        msg = 'Porfavor completa el formulario!'
    return render_template('register.html', msg=msg)

if __name__ =='__main__':
	app.run()
