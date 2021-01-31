# coding=utf-8
"""Passwordmanager es una aplicacion para gestion de contrasenas"""
import os
import time
import hashlib
import random
import string
import sys
import shutil
from getpass import getpass
from Crypto.Cipher import AES

SISTEMA = os.name

if SISTEMA == "posix":
    import pwd
    USUARIO=pwd.getpwuid(os.getuid())[0]

clsmode={
    "nt":"cls",
    "posix":"clear"
}

class Colores:
    """Colores del sistema"""
    morado = '\033[95m' #morado mostrat listas
    verde = '\033[92m' #verde todo correcto
    amarillo = '\033[93m' #amarillo warnings
    rojo = '\033[91m' #rojo errores
    blanco = '\033[0m' #blanco
    azul = '\033[94m' #azul

def titulo():
    """Titulo del programa"""
    print(Colores.amarillo+r"""
        (                                                                           
        )\ )                           (                                            
        (()/(   )       (  (       (    )\ )     )      )          ) (  (    (  (    
        /(_)| /( (  (  )\))(   (  )(  (()/( ___(    ( /(  (    ( /( )\))(  ))\ )(   
        (_)) )(_)))\ )\((_)()\  )\(()\  ((_))___)\  ')(_)) )\ ) )(_)|(_))\ /((_|()\  
        | _ ((_)_((_|(_)(()((_)((_)((_) _| |  _((_))((_)_ _(_/(((_)_ (()(_|_))  ((_) 
        |  _/ _` (_-<_-< V  V / _ \ '_/ _` | | '  \() _` | ' \)) _` / _` |/ -_)| '_| 
        |_| \__,_/__/__/\_/\_/\___/_| \__,_| |_|_|_|\__,_|_||_|\__,_\__, |\___||_|   
                                                                    |___/            
        """)

class Encriptacion:
    """"Classe para encriptacion"""
    def __init__(self):
        self.cifrado=hashlib.blake2s()
    def encriptar(self):
        """Funcion para encriptar los datos"""
        dirx=next(os.walk('Data'))[1]
        os.system(clsmode[SISTEMA])
        titulo()
        sitio = input('Agregar sitio a cual corresponde: ')
        while sitio in dirx:
            remplazar=input(Colores.amarillo+
            "Este sitio ya lo tienes registrado, deseas remplazar su informacion? S/N: ")
            if remplazar in ("s","S"):
                shutil.rmtree(os.path.join("Data",dirx[dirx.index(sitio)]))
                dirx=next(os.walk('Data'))[1]
            elif remplazar in ('N','n'):
                sitio =input('Agregar sitio a cual corresponde: ')

        usuario = input('Usuario o correo electronico: ')
        pswd = getpass('Contraseña:')
        password=getpass(Colores.azul+"Escribe tu master password: ").encode('utf-8')
        self.cifrado.update(password)
        data=f"{usuario}----{pswd}"
        filex= ''.join([random.choice(string.ascii_lowercase) for n in range(5)])
        try:
            os.mkdir(os.path.join("Data",sitio))
        except EnvironmentError:
            print(Colores.rojo+"No pudimos crear el directorio intenta de nuevo")
        while len(data) %16 !=0:
            data = ' '+data
        pss=self.cifrado.hexdigest()
        obj = AES.new(pss[0:32].encode('utf-8'), AES.MODE_CBC,pss[0:16].encode('utf-8'))
        ciphertext = obj.encrypt(data.encode("utf-8"))
        with open(f'Data/{sitio}/{filex}.JAHG', 'wb') as filex:
            filex.write(ciphertext)
        filex.close()
        print(Colores.verde+"Guardado con exito")
        time.sleep(2)

    def desencriptar(self):
        """Funcion para desencriptar los datos"""
        while True:
            self.cifrado=hashlib.blake2s()
            os.system(clsmode[SISTEMA])
            titulo()
            dirx=next(os.walk('Data'))[1]
            for index,name in enumerate(dirx):
                print(Colores.morado+f"{index+1}.-{name}\n")
            print("M.- Para volver al menu\n")
            print("Q.- Para salir\n")
            eleccion=input('>>>')
            try:
                eleccion=int(eleccion)
                if eleccion <= len(dirx):
                    password=getpass(Colores.azul+"Escribe tu master password: ").encode('utf-8')
                    self.cifrado.update(password)
                    pss=self.cifrado.hexdigest()
                    with open(os.path.join("Data",dirx[eleccion-1],
                    ''.join(next(os.walk(f'Data/{dirx[eleccion-1]}'))[2])), 'rb') as filex:
                        data=filex.read()
                    filex.close()
                    self.obj = AES.new(pss[0:32].encode('utf-8'),
                                        AES.MODE_CBC, pss[0:16].encode('utf-8'))
                    self.mostar(data)
                    time.sleep(5)
                else:
                    print(Colores.rojo+"No es una opcion valida")
                    time.sleep(1)
            except ValueError:
                if eleccion in ("q","Q"):
                    salir()
                elif eleccion in ("m","M"):
                    break
                else:
                    print(Colores.rojo+"No es una opcion valida")
                    time.sleep(1)

    def mostar(self,data):
        """ Metodo para mostrar usuarios desencriptados"""
        try:
            data=self.obj.decrypt(data)
            data=data.decode()
            data=data.strip()
            user=data[0:data.find("----")]
            password=data[data.find("----")+4:]
            print(f"Usuario: {user}\nContraseña: {password}")
        except UnicodeDecodeError:
            print(Colores.rojo+"Contrasena incorrecta")

def respaldar():
    """Metodo para respaldar informacion en un dispositivo fisico """
    if not os.listdir("Data"):
        print(Colores.rojo+"Aun no tienes informacion almacenada")
        time.sleep(1)
    else:
        dispositivo=input("Nombre del dispositivo >>> ")
        if SISTEMA == "posix":
            ruta=f"/media/{USUARIO}/{dispositivo}/"
            if os.path.isdir(ruta):
                ruta=ruta+"/pssmanager/Data"
                try:
                    print(Colores.amarillo+"Esto puede demorar un momento")
                    shutil.copytree("Data",ruta)
                    print(Colores.verde+"Completado")
                    time.sleep(1)
                except IOError:
                    print(Colores.rojo+"No se pudo copiar en el dispositivo")
                    time.sleep(1)
            else:
                print(Colores.rojo+"No existe el dispositivo")
                time.sleep(1)
        else:
            pass

def importar():
    """Metodo para pasar informacion de un dispositivo fisico """
    print(Colores.amarillo+"La estructura en tu dispositivo debe ser de la sig manera")
    print(Colores.blanco+"Dispositivo\pssmanager\Data")
    dispositivo=input("Nombre del dispositivo >>> ")
    if SISTEMA == "posix":
        ruta=f"/media/{USUARIO}/{dispositivo}/"
        if os.path.isdir(ruta):
            if os.path.isdir(f"{ruta}/pssmanager/Data"):
                for archivo in os.listdir(f"{ruta}/pssmanager/Data/"):
                    if archivo in os.listdir("Data"):
                        remplazar=input(Colores.amarillo+
                        f"El sitio {archivo} ya lo tienes registrado, deseas remplazar su informacion? S/N:")
                        if remplazar in ("s","S"):
                            shutil.rmtree(os.path.join("Data",archivo))
                            shutil.copytree(f"{ruta}/pssmanager/Data/{archivo}",f"Data/{archivo}")
                    else:
                        shutil.copytree(f"{ruta}/pssmanager/Data/{archivo}",f"Data/{archivo}")
                print(Colores.verde+"Completado")
                time.sleep(1)
            else:
                print(Colores.rojo+"Verifica el orden de tu dispositivo")
                time.sleep(1)
        else:
            print(Colores.rojo+"No existe el dispositivo")
            time.sleep(1)
    else:
        pass

def salir():
    """Metodo para salir"""
    os.system(clsmode[SISTEMA])
    sys.exit(0)

def main():
    """Metodo que llama al menu principal"""
    crypt=Encriptacion()
    opciones={  "Desencriptar cuenta":crypt.desencriptar,
                "Encriptar nueva cuenta": crypt.encriptar,
                "Respaldar en dispositivo":respaldar,
                "Importar informacion": importar,
                "Salir":salir
                }
    opciones_lista=["Desencriptar cuenta","Encriptar nueva cuenta","Respaldar en dispositivo","Importar informacion","Salir"]
    while True:
        os.system(clsmode[SISTEMA])
        titulo()
        for index,opcion in enumerate(opciones):
            print(Colores.morado+f"{index+1}.-{opcion}\n")
        eleccion=input(">>>")
        try:
            eleccion=int(eleccion)
            if eleccion <= len(opciones_lista):
                opciones[opciones_lista[eleccion-1]]()
            else:
                print(Colores.rojo+"No es una opcion valida")
                time.sleep(1)
        except ValueError:
            print(Colores.rojo+"No es una opcion valida")
            time.sleep(1)

if __name__ == "__main__":
    if os.path.isdir("Data"):
        sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=32, cols=100))
        main()
    else:
        try:
            sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=32, cols=100))
            os.mkdir("Data")
            main()
        except EnvironmentError:
            print(Colores.rojo+"No pudimos crear el fichero, intenda despues")
