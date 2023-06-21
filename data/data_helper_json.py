import json
import bcrypt as bc
from currencies import curr
import requests as rq
from decimal import Decimal

class DataHelper:
    def __init__(self):
        self.filepath='userpwd.json'
        global access_key
        access_key = 'f3a24b68620fab1336ea9d8b2b6fcbf4'

    def matchUserPass(self,user, password):
        
        with open('usuarios.json',"r") as f:
            serObj=f.read()
            res=json.loads(serObj)
            userList=res["lista_de_usuarios"]
            for ul in userList :
                if ul['usuario']==user:
                    if bc.checkpw(password.encode('utf-8'), ul['pwd'].encode('utf-8')): 
                        return ul['usuario'],ul['pwd']
                    else:
                        return ul['usuario'], None
            return None,None
        

    def matchUser(self, user):
        with open('usuarios.json', "r") as f:
            data = json.load(f)

        lista_usuarios = data["lista_de_usuarios"]
        for usuario_actual in lista_usuarios:
            if usuario_actual["usuario"] == user:
                return True  # El usuario ya existe
        return False  # El usuario no existe


    def isCurrCodeValid(self,currCode):
        if currCode in curr.keys():
            return True
        return False

    def agregar_cuenta(self, tipo_moneda, user):
            filename = user + ".json"
            accounts_des = {}
            with open(filename,"r") as f:
                file_content = f.read()
                accounts_des=json.loads(file_content)
            accounts_des.update({tipo_moneda:"0.00"})
            with open(filename,"w") as f:
                accounts_ser = json.dumps(accounts_des,indent=4)
                f.write(accounts_ser)

                print("Cuenta agregada exitosamente.")


    def saveUser(self, user, password):
        with open('usuarios.json',"r") as f:
            datos_json = json.load(f)
    
        nuevo_usuario = {"usuario": user, "pwd": password.decode('utf-8')}
        datos_json["lista_de_usuarios"].append(nuevo_usuario)
    
        # Guarda los datos en el archivo JSON
        with open('usuarios.json', "w") as archivo:
            json.dump(datos_json, archivo, indent=4)

        nombreArchivo = user + '.json'

        cuentaARS = { "ARS" : "0.00"}

        with open( nombreArchivo, "w") as archivo:
            json.dump(cuentaARS, archivo, indent=4)
        
        print("Archivo JSON creado exitosamente.")


        
    def modifyPassword(self, user, contraNueva):

        nombreArchivo = 'usuarios.json'

        with open (nombreArchivo, "r") as f: 
            datos_json = json.load(f)

            # Verifica si el archivo JSON tiene la lista de usuarios
            if "lista_de_usuarios" in datos_json:
                lista_usuarios = datos_json["lista_de_usuarios"]

            # Busca y modifica el campo "pwd" en cada usuario
            for usuario in lista_usuarios:
                if usuario["usuario"] == user:
                    usuario["pwd"] = contraNueva.decode('utf-8')
                    break

        # Guarda los datos actualizados en el archivo JSON
        with open(nombreArchivo, 'w') as archivo:
            json.dump(datos_json, archivo, indent=4)

        print("Contraseñas modificadas exitosamente.")



    def AccountExist(self ,user,currCode):
        filename = user + ".json"
        with open(filename,"r") as f:
            file_content = f.read()
            file_des=json.loads(file_content)
            if currCode in file_des.keys():
                return True
            else:
                return False
                

    def verificarMontoDisponible(self, user, codMoneda):
        
        nombreArchivo = user + '.json'

        with open (nombreArchivo, "r") as f: 
            montos =  json.load(f)

        if codMoneda in montos:
            monto = Decimal (montos[codMoneda])
            return monto
        else:
            return None
        


    def obtener_valor_moneda(self, codMoneda):
        valorMoneda_EUR= f"http://data.fixer.io/api/latest?access_key=" + access_key + "&symbols=" + codMoneda

        responseMoneda = rq.get(valorMoneda_EUR)
        responseMoneda_Json=responseMoneda.json()

        rates = responseMoneda_Json['rates']
        ratesMoneda = rates[codMoneda]

        ratesarg = self.obtenerValorARS()

        calculo = ratesarg / ratesMoneda
        resultadoDecimal = Decimal(calculo).quantize(Decimal('0.00'))
        
        return resultadoDecimal


    def obtenerValorARS(self):
        valorARS_EUR= f"http://data.fixer.io/api/latest?access_key=" + access_key + "&symbols=ARS"

        responseARS = rq.get(valorARS_EUR)
        responseARS_Json=responseARS.json()

        rates = responseARS_Json['rates']
        ratesARS = rates['ARS']

        return ratesARS
    

    def calcularCantidadARS(self, cantidad, codMoneda):

        valorMoneda = self.obtener_valor_moneda(codMoneda)

        cantidad_ARS = Decimal(valorMoneda * cantidad).quantize(Decimal('0.00'))

        return cantidad_ARS
    
    
    def TransaccionCompra(self, user, cantidadARS, codMoneda,  cantidadMoneda):
        nombreArchivo = user + '.json'

        with open(nombreArchivo, 'r') as f:
            datos = json.load(f)

        ARSenCuenta = Decimal(datos['ARS'])
        MonedaEnCuenta = Decimal(datos[codMoneda])

        cantidadARS = Decimal(cantidadARS)
        cantidadMoneda = Decimal(cantidadMoneda)

        ARSActualizado = ARSenCuenta - cantidadARS
        MonedaActualizado = MonedaEnCuenta + cantidadMoneda

        # Actualizar los valores de ARS y USD
        datos['ARS'] = str(ARSActualizado)
        datos[codMoneda] = str(MonedaActualizado)

        with open(nombreArchivo, 'w') as f:
            json.dump(datos, f, indent=4)


    def TransaccionVenta(self, user, cantidadARS, codMoneda,  cantidadMoneda):
        nombreArchivo = user + '.json'

        with open(nombreArchivo, 'r') as f:
            datos = json.load(f)

        ARSenCuenta = Decimal(datos['ARS'])
        MonedaEnCuenta = Decimal(datos[codMoneda])

        cantidadARS = Decimal(cantidadARS)
        cantidadMoneda = Decimal(cantidadMoneda)

        ARSActualizado = ARSenCuenta + cantidadARS
        MonedaActualizado = MonedaEnCuenta - cantidadMoneda

        # Actualizar los valores de ARS y USD
        datos['ARS'] = str(ARSActualizado)
        datos[codMoneda] = str(MonedaActualizado)

        with open(nombreArchivo, 'w') as f:
            json.dump(datos, f, indent=4)

    def Depositar(self, user, cantidadARS):
        nombreArchivo = user + '.json'

        with open(nombreArchivo, 'r') as f:
            datos = json.load(f)

        ARSenCuenta = Decimal(datos['ARS'])

        cantidadARS = Decimal(cantidadARS)

        ARSActualizado = ARSenCuenta + cantidadARS

        # Actualizar los valores de ARS y USD
        datos['ARS'] = str(ARSActualizado)

        with open(nombreArchivo, 'w') as f:
            json.dump(datos, f, indent=4)

        return ARSActualizado


    def mostrarCurrencies(self):
        from currencies import curr
        resultados = []
        for clave, valor in curr.items():
            resultado = clave + ": " + valor 
            resultados.append(resultado)
        return resultados

    def consultarSaldos(self, user):
        nombreArchivo = user + '.json'
        with open(nombreArchivo) as archivo:
            datos = json.load(archivo)
        return datos


    






        


