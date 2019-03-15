import math, copy
from treelib import Node, Tree
import json

class Fila():
    pass

class Atributo():
    def __init__(self):
        self.valores = {}
        self.merito = 0
        self.total = 0

class Elemento():
     def __init__(self):
        self.total = 0
        self.valores = {
            "positivos": 0,
            "negativos": 0
        }

def infor(p,n):
    if p != 0:
        x = -p * math.log(p, 2)
    else:
        x = 0

    if n != 0:
        y = -n * math.log(n,2)
    else:
        y = 0

    return x + y

def crearListas(listaAtributos, listaEjemplos, stringListaAtributos):
    fAtr = open("AtributosJuego.txt", "r")
    for x in fAtr.read().rstrip().split(","):
        listaAtributos[x] = Atributo()
        stringListaAtributos.append(x)
    
    fJue = open("Juego.txt", "r")

    for x in fJue:
        lisX = x.rstrip().split(",")
        f = Fila()
        for y in listaAtributos:

            setattr(f, y, lisX[0])

            if not lisX[0] in listaAtributos[y].valores:
                listaAtributos[y].valores[lisX[0]] = Elemento()

            if lisX[len(lisX) - 1] == "si":
                listaAtributos[y].valores[lisX[0]].valores["positivos"] += 1
            else:
                listaAtributos[y].valores[lisX[0]].valores["negativos"] += 1

            listaAtributos[y].valores[lisX[0]].total += 1
            listaAtributos[y].total += 1
            del lisX[0]
        listaEjemplos.append(f)

def calcularMerito(listaAtributos, listaEjemplos):
    for a in listaAtributos:
        if a != "Jugar":
            listaAtributos[a].merito = 0 
            for v in listaAtributos[a].valores:           
                if listaAtributos[a].total != 0 and listaAtributos[a].valores[v].total != 0:
                    listaAtributos[a].merito += (listaAtributos[a].valores[v].total/listaAtributos[a].total) * infor((listaAtributos[a].valores[v].valores["positivos"]/listaAtributos[a].valores[v].total), (listaAtributos[a].valores[v].valores["negativos"]/listaAtributos[a].valores[v].total))
                else:
                    listaAtributos[a].merito = math.inf
        else:
            listaAtributos[a].merito = math.inf

def id3(listaAtributos, listaEjemplos, arbol, padre):
    if len(listaEjemplos) == 0:
        return 
    
    for eje in listaEjemplos:
        if eje.Jugar != "si":
            break    
    else:
        arbol.create_node("si", padre + "." + "si", padre)
        return

    for eje in listaEjemplos:
        if eje.Jugar != "no":
            break    
    else:
        arbol.create_node("no", padre + "." + "no", padre)
        return

    if len(listaAtributos) == 0:
        return "error"
        
    calcularMerito(listaAtributos, listaEjemplos)

    sortListaAtributos = sorted(listaAtributos.items(), key=lambda kv: kv[1].merito, reverse=False)

    atributo = sortListaAtributos[0][0]
    del listaAtributos[atributo]

    if padre != None:
        arbol.create_node(atributo, padre + "." + atributo, parent=padre)
    else:
        arbol.create_node(atributo, atributo, parent=padre)

    for v in sortListaAtributos[0][1].valores.keys():
        objLista = rehacerListas(v, atributo, copy.deepcopy(listaAtributos), copy.deepcopy(listaEjemplos))
        if padre != None:  
            arbol.create_node(v, padre + "." + atributo + "." + v, padre + "." + atributo)
            id3(copy.deepcopy(objLista["listaAtributos"]), objLista["listaEjemplos"], arbol, padre + "." + atributo + "." + v)
        else:
            arbol.create_node(v, atributo + "." + v, atributo)
            id3(copy.deepcopy(objLista["listaAtributos"]), objLista["listaEjemplos"], arbol, atributo + "." + v)


def rehacerListas(valor, atributo, listaAtributos, listaEjemplos):
    nuevaListaEjemplos = []

    for x in listaEjemplos:
        val = getattr(x, atributo)
        if (val == valor):
            nuevaListaEjemplos.append(x)
        else:
            for y in listaAtributos:
                if listaAtributos.get(y) != None:
                    if getattr(x, "Jugar") == "si":                 
                        listaAtributos[y].valores[getattr(x, y)].valores["positivos"] -= 1
                    else:
                        listaAtributos[y].valores[getattr(x, y)].valores["negativos"] -= 1

                    listaAtributos[y].valores[getattr(x, y)].total -= 1
                    listaAtributos[y].total -= 1


    return {
        "listaAtributos": listaAtributos,
        "listaEjemplos": nuevaListaEjemplos
    }

def realizarBusqueda(arbol, atributos):

    continuar = True

    while continuar:
        print("Introducir parametros para la busqueda:")

        busqueda = {}
        for a in atributos:
            print(a + ": ", end="")
            busqueda[a] = input().lower()

        print("\n")

        resultado = recRealizarBusqueda(arbol, busqueda, arbol.root)

        if resultado == None:
            print("No contamos con datos suficientes")
        elif resultado == "si":
            print("La respuesta es Si")
        elif resultado == "no":
            print("La respuesta es No")

        print("\n¿Desea realizar otra consulta?(si/no) ", end="")
        respuesta = input()

        if respuesta.lower() != "si":
            continuar = False
    else:
        print("\nSaliendo del programa")

def recRealizarBusqueda(arbol, atributos, tag):
    
    if tag == "si":
        return "si"
    elif tag == "no":
        return "no"

    try:
        siguiente = arbol.children(arbol.root + "." + atributos[tag])

        return recRealizarBusqueda(arbol.subtree(siguiente[0].identifier), atributos, siguiente[0].tag)
    except:
        return None

listaAtributos = {}
listaEjemplos = []
stringListaAtributos = []
arbol = Tree()

crearListas(listaAtributos, listaEjemplos, stringListaAtributos)  

id3(copy.deepcopy(listaAtributos), copy.deepcopy(listaEjemplos), arbol, None)

del stringListaAtributos[len(stringListaAtributos) - 1]

arbol.show(line_type="ascii-em")

realizarBusqueda(arbol, stringListaAtributos)

