from business.admin import Verifier
import getpass
import sys


class App:
    def __init__(self):
        self.user = ''
        self.password = ''



    def Run (self):
        print('Bienvenido')

        App.iniciarSesion(self)

        print('Elija una opcion:')
        print('[1] Crear un usuario nuevo')
        print('[2] Modificar contraseña')
        print('[3] Agregar cuenta')
        print('[4] Depositar')
        print('[5] Comprar')
        print('[6] Vender')
        print('[7] Mostrar lista de monedas de cambio')
        print('[8] Consultar Saldos')
        self.opcion = input('')

        if self.opcion == '1':
             App.crearUsuario()
        if self.opcion == '2':
             App.Modificar(self)
        if self.opcion == '3':
             App.AgregarCuenta(self)
        if self.opcion == '4':
             App.Depositar(self)
        if self.opcion == '5':
             App.Comprar(self)
        if self.opcion == '6':
             App.Vender(self)
        if self.opcion == '7':
            myVerifier = Verifier(self.user , self.password)
            currencies = myVerifier.mostrarCurrencies()
            for curr in currencies:
                print(curr)
        if self.opcion == '8':
             myVerifier = Verifier(self.user , self.password)
             saldos = myVerifier.consultarSaldo()
             for saldo in saldos:
                print(saldo)
             
             


    def crearUsuario():
        usuarioNuevo = input('Por favor ingrese un nombre de usuario: ')
        contraseñaNueva = getpass.getpass('Ahora ingrese una contraseña: ')

        myVerifier = Verifier(usuarioNuevo , contraseñaNueva)

        try:
            dev = myVerifier.VerificarDatosIngresados()
            try:
                verificarUsuarioExistente = myVerifier.VerificarUsuarioExistente()
                print('Usuario disponible!')
                myVerifier.guardarUsuarioNuevo()
                print('Los datos han sido guardados en el archivo')
            except Exception as e:
                print(e.args[0])    
        except Exception as e:
                print(e.args[0])



    def iniciarSesion(self):
            self.user = input('Ingrese su nombre de usuario: ')
            self.password = getpass.getpass('Ingrese contraseña: ')

            myVerifier = Verifier(self.user , self.password)

            try:
                print ("\n")
                dev = myVerifier.VerificarDatosIngresados()   
            except Exception as e:
                 print(e.args[0])
                 sys.exit(1)

            try:
                dev = myVerifier.Verifymatch()
                print("Datos Correctos, Bienvenido!")
            except Exception as e:
                print(e.args[0])
                sys.exit(1)


    def Modificar(self):
        contraseñaNueva = getpass.getpass('Ingrese una contraseña nueva: ')

        if contraseñaNueva == "":
            print("Es obligatorio ingresar una contraseña")
            sys.exit(1)

        myVerifier = Verifier(self.user , contraseñaNueva)  

        try:
            myVerifier.modificarContraseña()
        except Exception as e:
            print(e.args[0])


    def AgregarCuenta(self):
        TipoCuenta = input('Ingrese el tipo de cuenta que desea abrir: ')

        try:
            myVerifier = Verifier(self.user , self.password)
            myVerifier.AgregarCuenta(self.user, TipoCuenta)
        except Exception as e:
            print(e.args[0])

    def Comprar(self):
        codMonedaComprar = input('Ingrese el codigo de la moneda que desea comprar: ').upper()

        try:
            if codMonedaComprar == 'ARS':
                raise Exception('No puede comprar ARS, si desea Depositar vuelva al menu principal')
            myVerifier = Verifier(self.user , self.password)
            myVerifier.VerificarTipoMoneda(codMonedaComprar)
            myVerifier.VerificarCuentaExistente(codMonedaComprar)

            cantidad = input ('Cuantos ' + codMonedaComprar + ' desea comprar?: ')

            codMonedaVender = 'ARS'

            myVerifier.TransaccionCompra(cantidad, codMonedaComprar, codMonedaVender)
        except Exception as e:
            print(e.args[0])

    def Vender(self):
        codMonedaVender = input('Ingrese el codigo de la moneda que desea vender: ').upper()

        try:
            if codMonedaVender == 'ARS':
                raise Exception('Solo puede vender monedas extranjeras!')
            myVerifier = Verifier(self.user , self.password)
            myVerifier.VerificarTipoMoneda(codMonedaVender)
            myVerifier.VerificarCuentaExistente(codMonedaVender)

            cantidad = input ('Cuantos ' + codMonedaVender + ' desea vender?: ')

            codMonedaComprar = 'ARS'

            myVerifier.TransaccionVenta(cantidad, codMonedaComprar, codMonedaVender)
        except Exception as e:
            print(e.args[0])

    def Depositar(self):
        try:
            codMonedaComprar = 'ARS'
            myVerifier = Verifier(self.user , self.password)
            myVerifier.VerificarTipoMoneda(codMonedaComprar)
            myVerifier.VerificarCuentaExistente(codMonedaComprar)

            cantidad = input ('Cuantos ' + codMonedaComprar + ' desea Depositar?: ')

            codMoneda = 'ARS'

            myVerifier.Deposito(cantidad, codMoneda)
        except Exception as e:
            print(e.args[0])

