from data.data_helper_json import DataHelper
import bcrypt as bc
from decimal import Decimal

class Verifier:
    def __init__(self,user,password):
        self.user = user
        self.password = password

    def VerificarDatosIngresados(self):
        
        if self.user == '':
            raise Exception( "Es obligatorio ingresar un usuario")
        if self.password == '':
            raise Exception("Es obligatorio ingresar una contraseña")

        self.password =self.password.lower() 


    def Verifymatch(self):

        myDataHelper = DataHelper()
        ruser, rpassword = myDataHelper.matchUserPass(self.user, self.password)
        
        if ruser is None:
            raise Exception("Usuario no encontrado")
        elif rpassword is None:
            raise Exception("Contraseña incorrecta")
        else:
            return 
       

    def VerificarUsuarioExistente(self):
        myDataHelper = DataHelper()
        ruser = myDataHelper.matchUser(self.user)
        
        if ruser is False:
            return
        else:
            raise Exception("El usuario ya esta en uso!")
  

    def guardarUsuarioNuevo(self):
        myDataHelper = DataHelper()
        self.password = bc.hashpw(self.password.encode('utf-8'),bc.gensalt())
        dev = myDataHelper.saveUser(self.user, self.password)
        return


    def modificarContraseña(self):
        
        myDataHelper = DataHelper()
        contraNueva = bc.hashpw(self.password.encode('utf-8'),bc.gensalt())
        modificar = myDataHelper.modifyPassword(self.user, contraNueva)

        if modificar is None:
            raise Exception("Su contraseña fue modificada.")
        else:
            raise Exception("Hubo un error.")


    def AgregarCuenta(self, user, tipoCuenta):

        myDataHelper = DataHelper()

        tipoCuenta=tipoCuenta.lstrip().rstrip().upper()

        if myDataHelper.isCurrCodeValid(tipoCuenta) == False:
            raise Exception("Codigo de moneda no valido, consulte la lista de monedas en el menu principal!")
        
        if myDataHelper.AccountExist(self.user, tipoCuenta) == True:
            raise Exception("Ya Existe la cuenta que desea crear")

        myDataHelper.agregar_cuenta(tipoCuenta, user)


    def VerificarTipoMoneda(self, codMoneda):

        myDataHelper = DataHelper()
        response = myDataHelper.isCurrCodeValid(codMoneda)

        if response is True:
            return
        else:
            raise Exception ("No se encontro esa moneda")
        

    def VerificarCuentaExistente(self, codMoneda):
        myDataHelper = DataHelper()
        response = myDataHelper.AccountExist(self.user, codMoneda)
        
        if response is True:
            return
        else:
            raise Exception("Usted no tiene cuenta en " + codMoneda)
        

    def Deposito(self, cantidad, codMoneda):
        cantidadDecimal = Decimal(cantidad).quantize(Decimal('0.00'))
        myDataHelper = DataHelper()

        ARSactualizado = myDataHelper.Depositar(self.user, cantidadDecimal)

        if ARSactualizado >= cantidadDecimal:
            raise Exception("Transaccion completada! su saldo actual es de " + str(ARSactualizado))
        else:
            raise Exception("Hubo un error.")
            
        

    def TransaccionCompra(self, cantidad, codMonedaComprar, codMonedaVender):
        cantidadDecimal = Decimal(cantidad).quantize(Decimal('0.00'))
        myDataHelper = DataHelper()
        ARSenCuenta = myDataHelper.verificarMontoDisponible(self.user, codMonedaVender)
        cantidadSolicitada = myDataHelper.calcularCantidadARS(cantidadDecimal, codMonedaComprar)

        if ARSenCuenta >= cantidadSolicitada:
            myDataHelper.TransaccionCompra(self.user, cantidadSolicitada, codMonedaComprar, cantidad)
            raise Exception("Transaccion completada!")
        else:
            raise Exception("No tiene fondos suficientes para realizar la operacion")
        

    def TransaccionVenta(self, cantidad, codMonedaComprar, codMonedaVender):
        cantidadDecimal = Decimal(cantidad).quantize(Decimal('0.00'))
        myDataHelper = DataHelper()
        saldoDisponible = myDataHelper.verificarMontoDisponible(self.user, codMonedaVender)
        cantidadVender = myDataHelper.calcularCantidadARS(cantidadDecimal, codMonedaVender)

        if saldoDisponible >= cantidadDecimal:
            myDataHelper.TransaccionVenta(self.user, cantidadVender, codMonedaVender, cantidad)
            raise Exception("Transaccion completada!")
        else:
            raise Exception("No tiene fondos suficientes para realizar la operacion")
        

    def mostrarCurrencies(self):
        myDataHelper = DataHelper()
        currencies = myDataHelper.mostrarCurrencies()

        return currencies

    def consultarSaldo(self):
        myDataHelper = DataHelper()
        response = myDataHelper.consultarSaldos(self.user)

        saldos = []
        for moneda, saldo in response.items():
            saldos.append(f"SALDO {moneda}: {saldo}")
        return saldos