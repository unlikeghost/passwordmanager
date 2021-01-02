# coding=utf-8
import os,time,hashlib
from Crypto.Cipher import AES
from getpass import getpass
import random,string,sys,shutil

sistema = os.name

clsmode={
    "nt":"cls",
    "posix":"clear"
}

class colores:
    morado = '\033[95m' #morado mostrat listas
    verde = '\033[92m' #verde todo correcto
    amarillo = '\033[93m' #amarillo warnings
    rojo = '\033[91m' #rojo errores
    blanco = '\033[0m' #blanco
    azul = '\033[94m' #azul

def titulo():
    print(colores.amarillo+r"""
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

class encriptacion:
    def __init__(self):
        self.cifrado=hashlib.blake2s()
    def encriptar(self):
        dir=next(os.walk('Data'))[1]
        os.system(clsmode[sistema])
        titulo()
        sitio = input('Agregar sitio a cual corresponde: ')
        while sitio in dir:
            remplazar=input(colores.amarillo+"Este sitio ya lo tienes registrado, deseas remplazar su informacion? S/N: ")
            if remplazar == "S" or remplazar=="s":
                shutil.rmtree(os.path.join("Data",dir[dir.index(sitio)]))
                break
                # os.rmdir(os.path.join(os.pos.path.join("Data",dir[dir.index(sitio)]))ath.join("Data",dir[dir.index(sitio)])))
            elif remplazar == "N" or remplazar=="n":
                sitio =input('Agregar sitio a cual corresponde: ')

        usuario = input('Usuario o correo electronico: ')
        pswd = getpass('Contraseña:')
        password=getpass(colores.azul+"Escribe tu master password: ").encode('utf-8')
        
        self.cifrado.update(password)
        data=f"{usuario}----{pswd}"
        filex= ''.join([random.choice(string.ascii_lowercase) for n in range(5)])

        try:
            os.mkdir(os.path.join("Data",sitio))
        except Exception as e:
            print(e)

        while len(data) %16 !=0:
            data = ' '+data

        pss=self.cifrado.hexdigest()
        obj = AES.new(pss[0:32], AES.MODE_CBC,pss[0:16])
        ciphertext = obj.encrypt(data)

        with open(f'Data/{sitio}/{filex}.JAHG', 'wb') as f:
            f.write(ciphertext)
        print(colores.verde+"Guardado con exito")
        time.sleep(2)

    def desencriptar(self):
        while True:
            self.cifrado=hashlib.blake2s()
            os.system(clsmode[sistema])
            titulo()
            dir=next(os.walk('Data'))[1]
            for index,name in enumerate(dir):
                print(colores.morado+f"{index+1}.-{name}\n")
            print("M.- Para volver al menu\n")
            print("Q.- Para salir\n")
            eleccion=input('>>>')

            try:
                eleccion=int(eleccion)
                if eleccion <= len(dir):
                    password=getpass(colores.azul+"Escribe tu master password: ").encode('utf-8')
                    self.cifrado.update(password)
                    pss=self.cifrado.hexdigest()
                    with open(os.path.join("Data",dir[eleccion-1], ''.join(next(os.walk(f'Data/{dir[eleccion-1]}'))[2])), 'rb') as f:
                        data=f.read()
                    f.close()
                    self.obj = AES.new(pss[0:32], AES.MODE_CBC, pss[0:16])
                    self.mostar(data)
                    time.sleep(5)
                else:
                    print(colores.rojo+"No es una opcion valida")
                    time.sleep(1)
            except:
                if eleccion == "M" or eleccion == "m":
                    break
                elif eleccion == "Q" or eleccion == "q":
                    self.salir()
                else:
                    print(colores.rojo+"No es una opcion valida")
                    time.sleep(1)

    def mostar(self,data):
        try:
            data=self.obj.decrypt(data)
            data=data.decode()
            data=data.strip()
            user=data[0:data.find("----")]
            password=data[data.find("----")+4:]
            print(f"Usuario: {user}\nContraseña: {password}")
        except UnicodeDecodeError:
            print(colores.rojo+"Contrasena incorrecta")
    def salir(self):
        os.system(clsmode[sistema])
        exit(0)
    

def main():
    crypt=encriptacion()
    opciones={  "Desencriptar cuenta":crypt.desencriptar,
                "Encriptar nueva cuenta": crypt.encriptar,
                "Salir":crypt.salir
                }
    opcionesLista=["Desencriptar cuenta","Encriptar nueva cuenta","Salir"]

    while True:
        os.system(clsmode[sistema])
        titulo()
        for index,opcion in enumerate(opciones):
            print(colores.morado+f"{index+1}.-{opcion}\n")
        eleccion=input(">>>")
        try:
            eleccion=int(eleccion)
            if eleccion <= len(opcionesLista):
                opciones[opcionesLista[eleccion-1]]()
            else:
                print(colores.rojo+"No es una opcion valida")
                time.sleep(1)  
        except ValueError:
            print(colores.rojo+"No es una opcion valida")
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
        except Exception as e:
            print(e)