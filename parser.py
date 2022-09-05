

class Variables:   #una clase para controlar las variables

    def __init__(self): #inicializa la clase generando una lista de variables vacia
        self.variables = {}

    def nueva_var(self, nombre, valor=None): #agrega una variable a la lista
        self.variables[nombre] = valor

    def existe_var(self, var): #retorna verdadero o falso si la variable existe
        if var in self.variables:
            return True
        else:
            return False

    def asignar_tipo(self, var, valor):
        if Variables.existe_var(var) == True:
            self.variables[var] = type(valor)
            return True
        else:
            print("Hay un error en sintax!")
            return False


class Funciones_Usuario:  #una clase que controla las funciones creadas por usuario

    def __init__(self):
        self.funciones = {}

    def nueva_funcion(self, nombre, vars:list):
        self.funciones[nombre] = vars

    def existe_func(self, nombre):
        if nombre in self.funciones:
            return True
        else:
            return False
    

class Funciones_Predeterminadas:

    def __init__(self):
        self.funciones_tipo = {"jump":99, "jumpTo":"jumpTo", "veer":["left", "rigt", "around"], "look":["north", "south", "west", "east"],
        "drop":99, "grab":99, "get":99, "free":99, "pop":99, "walk":"walk", "isfacing":["north", "south", "west", "east"],
        "isValid":"isValid","canWalk":"canWalk","not":["isfacing", "isValid", "canWalk"]}


    def tipo_func(self, func, valor, valor2=None):
        tipo = type(valor)
        tipo2 = type(valor2)

        if func in self.funciones_tipo:
            if type(self.funciones_tipo[func]) == int:
                if tipo == int:
                    return True
                else:
                    return False

            elif type(self.funciones_tipo[func]) == list:
                if tipo == str:
                    if valor in self.funciones_tipo[func]:
                        return True
                    else:
                        return False
                else:
                    return False

            elif self.funciones_tipo[func] == "walk":
                if valor2 == None:
                    if tipo == int:
                        return True
                    else:
                        return False
                else:
                    if tipo == str:
                        if valor in ["north", "south", "west", "east"]:
                            if tipo2 == int:
                                return True
                            else:
                                return False
                        else:
                            return False
                    return False 

            elif self.funciones_tipo[func] == "isValid":
                if tipo == str:
                    if valor in ["walk", "jump", "grab", "pop", "pick", "free", "drop"]:
                        if Funciones_Predeterminadas.tipo_func(valor, valor2) == True:
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False

            elif self.funciones_tipo[func] == "canWalk":
                if valor2 != None:
                    if tipo == str:
                        if valor in ["north", "south", "west", "east", "front", "right", "left", "back"]:
                            if tipo2 == int:
                                return True
                            else:
                                return False
                        else:
                            return False
                else:
                    return False 

            elif self.funciones_tipo[func] == "jumpTo":
                if valor2 != None:
                    if tipo == int:
                        if tipo2 == int:
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
        else:
            return False
        

class Interpretador:

    def __init__(self, code):
        self.code = code.replace(" ","").replace("CORP", "CORP;")
        self.godcode = code.split(";")
        self.palabras_reservadas = ["PROG","GORP","var","PROC","CORP","walk","jump","jumpTo", "veer","look","drop","grab","get","free","pop","walk","if","else","fi",
        "while","do","od","repeatTimes","per","isfacing","isValid","canWalk","not", "{","}"]
        self.palabra_reservada_bloq =["PROG","GORP","var","PROC","CORP","if","else","fi","while","do","od","repeatTimes","per"]
        self.palabra_reservada_func = ["walk","jump","jumpTo", "veer","look","drop","grab","get","free","pop","walk","isfacing",
        "isValid","canWalk","not"] 
        self.variables = Variables()
        self.funciones_usuario = Funciones_Usuario()
        self.funciones_predeterminadas = Funciones_Predeterminadas()
        self.proctimes = 0
        self.corptimes = 0
        self.whilecorret = 0
        self.ifcorrect = 0
        self.repeattimescorrect = 0
        self.funciones = []

    def revisar(self):
        if self.code.startswith("PROG") and self.code.endswith("GORP"):
            self.godcode[0] = self.godcode[0].replace("PROG", "")
            self.godcode[-1] = self.godcode[len(self.godcode) - 1].replace("GORP", "")
            for element in self.godcode:
                for palabra_reservada in self.palabras_reservadas:
                    if palabra_reservada in element:   #si hay palabra reservada
                        if palabra_reservada in self.palabra_reservada_bloq:
                            if palabra_reservada == "PROG":
                                print("Hay un error en el syntax!")
                                break
                            elif palabra_reservada == "GORP":
                                print("Hay un error en el syntax!")
                                break
                            elif palabra_reservada == "var":
                                for variable in element.split("var")[1]:
                                    if variable != ",":
                                        self.variables.nueva_var(variable)
                            elif palabra_reservada == "PROC":
                                self.proctimes +=1
                                if self.proctimes >1:
                                    print("Hay un error en el syntax!")
                                    break
                                else:
                                    funcion = ""
                                    if element.startswith("PROC") and element.endswith("CORP"):
                                        funcion = element
                                    elif element.startswith("PROC") and element.endswith("CORP") == False:
                                        ix = self.godcode.index(element)
                                        Corpfound = False
                                        funcion = ""
                                        elemento = element
                                        while Corpfound == False:
                                            if element.endswith("CORP"):
                                                Corpfound = True
                                            else:
                                                elemento = self.godcode[ix]
                                                ix += 1
                                                funcion = funcion + elemento
                                    if funcion != "":
                                        self.funciones.append(funcion)
                                        funcionsplit = funcion.split(")")
                                        nombreyvar = funcionsplit[0].split("(")
                                        nombre = nombreyvar[0]
                                        vars = []
                                        for cosa in nombreyvar[1]:
                                            if cosa != " " and cosa != ",":
                                                vars.append(cosa)
                                        self.funciones_usuario.nueva_funcion(nombre,vars)

                            elif palabra_reservada == "CORP":
                                self.corptimes +=1
                                if self.corptimes >1:
                                    print("Hay un error en el syntax!")
                                    break
                            elif palabra_reservada == "while":
                                self.whilecorret += 2
                                if self.whilecorret >2:
                                    print("Hay un error en el syntax!")
                                    break
                            
                            elif palabra_reservada == "do":
                                self.whilecorret -= 1
                                if self.whilecorret >1:
                                    print("Hay un error en el syntax!")
                                    break

                            elif palabra_reservada == "od":
                                self.whilecorret -= 1
                                if self.whilecorret >0:
                                    print("Hay un error en el syntax!")
                                    break

                            elif palabra_reservada == "if":
                                self.ifcorrect += 1
                                if self.ifcorrect > 1:
                                    print("Hay un error en el syntax!")
                                    break

                            elif palabra_reservada == "fi":
                                self.ifcorrect -= 1
                                if self.ifcorrect > 0:
                                    print("Hay un error en el syntax!")
                                    break
                                
                            elif palabra_reservada == "repeatTimes":
                                self.repeattimescorrect += 1
                                if self.repeattimescorrect > 1:
                                    print("Hay un error en el syntax!")
                                    break

                            elif palabra_reservada == "per":
                                self.repeattimescorrect -= 1
                                if self.repeattimescorrect > 0:
                                    print("Hay un error en el syntax!")
                                    break         
                        elif palabra_reservada in self.palabra_reservada_func:
                            times = 0
                            for funcion in self.palabra_reservada_func:
                                if funcion in element:
                                    times += 1
                            if times > 1:
                                print("Hay un error en el syntax!")
                                break
                for nombre_func in self.funciones_usuario.funciones.keys():
                    if nombre_func in element:
                        for funcione in self.funciones:
                            if nombre_func in funcione:
                                vartouse = element.split(str(nombre_func))
                                listavars = (vartouse[1].split(")")).replace("(","")
                                bars = []
                                for variable in listavars[0]:
                                    if variable != "," and variable != " ":
                                        bars.append(variable)

                                varsnot = self.funciones_usuario.funciones[nombre_func]
                                k = 0
                                while k < len(varsnot):
                                    funcione.replace(nombre_func, "")
                                    funcione.replace(varsnot[k], bars[k])
                                    funcione.replace("", nombre_func)
                                    k+=1

                                for palabra_reservada in self.palabra_reservada_func:
                                    if palabra_reservada in funcione:
                                        listap = funcione.split(palabra_reservada)
                                        listap = (listap[1].split(")")).replace("(", "")
                                        varparafunc = []
                                        for a in listap[0]:
                                            if a != "," and a != " ":
                                                varparafunc.append(a)
                                        if len(varparafunc) == 1:
                                            if self.funciones_predeterminadas.tipo_func(palabra_reservada, varparafunc[0]) != True:
                                                print("Hay un error en el syntax!")
                                                break
                                        elif len(varparafunc) == 2:
                                            if self.funciones_predeterminadas.tipo_func(palabra_reservada, varparafunc[0], varparafunc[1]) != True:
                                                print("Hay un error en el syntax!")
                                                break
                                        else:
                                            print("Hay un error en el syntax!")
                                            break        
                            else:    
                                print("Hay un error en el syntax!")
                                break               
                        
        else:
            print("Hay un error en el syntax!")
            
            
interpretador = Interpretador(input("Ingrese el codigo: "))

interpretador.revisar()
            

