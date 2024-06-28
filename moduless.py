from pathlib import Path
import os 
import csv
import json
home = Path(__file__).parent
archivocsv = Path(home/'mandarina.csv')
rutajson = Path(home/'archivo.json')

menup = ['Ver Listado de Pinturas',
         'Buscar Pintura', 
         'Agregar Pintura', 
         'Eliminar Pintura',
         'Exportar Pinturas',
         'SALIR']

def menux(menup):
    #menu del programa
    for ind, opt in enumerate(menup):
        print(f'{ind + 1}. {opt}')


def respuesta():
    resp = input('Ingresa una opción\n')
    return resp

def no_válida():
    print('...Opción no válida!\n')

def existe_json(r):
    if not r.exists():
        r.touch()

def leer_json(r):
    if r.stat().st_size == 0:
        lis = []
        return lis
    with open(r, mode='r') as stream:
        lis = json.load(stream)
    return lis

def pedir_dato():
    okey = ['si', 's', 'yes', 'y']
    while True:
        dato = input('Ingresa lo requerido:\n$')
        ans = input(f'{dato.upper()}\n¿Es correcto?\n(si/no)\n').lower()
        if ans in okey:
            break
    return dato.upper()

def pedir_datos():
    lis = leer_json(rutajson)
    if lis == []:
        code =380560
    else:
        codes = []
        for pinturas in lis:
            codes.append(pinturas["codigo"])
        code = max(codes)+1
    print('Nombre del color:\n')
    color_p = pedir_dato()
    print('Tipo de pintura:\n')
    tipo = pedir_dato()
    print('Valor de la pintura:$\n')
    price = pedir_dato()
    print('Ingresa el stock:\n')
    stock = pedir_dato()
    return {"codigo": code,
             "color": color_p,
            "tipo": tipo,
            "precio": int(price),
            "stock": int(stock)}

def cargar_json(r, d):
    '''
    r = ruta hacia un json
    d = data en formato {}
    '''
    with open(r, mode='w') as stream:
        json.dump(d, stream)

def buscar_pintura():
    dato = input('Ingresa el codigo o color de pintura:\n')
    return dato

def filtro_pintura(r, x):
    '''x= codigo en formato str
    r= ruta json'''
    lis = leer_json(r)
    if lis == []:
        print('Pintura no encontrada!\n')
    else:
        flag = False
        for pinturas in lis:
            if x == str(pinturas["codigo"]) or x.upper() in pinturas['color']:
                print(f'codigo: {pinturas["codigo"]}')
                print(f'color: {pinturas["color"]}')
                print(f'tipo:{pinturas["tipo"]}')
                print(f'precio:{pinturas["precio"]}')
                print(f'stock:{pinturas["stock"]}')
                flag = True
        if not flag:
            print('...No hay coincidencia en tu busqueda')

def pedir_codigo():
    dato = input('Ingresa el codigo:\n$')
    return dato

def eliminar_pintura(r, x):
    lis = leer_json(r)
    if lis == []:
        print('archivo vacío\n')
    else:
        for pinturas in lis:
            if str(pinturas["codigo"]) == x:
                lis.remove(pinturas)
                cargar_json(rutajson, lis)

def total_stock(r):
    if r.stat().st_size == 0:
        print('No hay datos en el archivo')
    else:
        total = 0
        with open(r, mode='r') as stream:
            lis = json.load(stream)
            for pinturas in lis:
                total += pinturas["stock"]
        print(f'El total de STOCK es: {total}')

def exportar(r, c):
    data = []
    with open(r, mode='r') as stream:
        lis = json.load(stream)
        for pinturas in lis:
            data.append([pinturas["codigo"],
                        pinturas["color"],
                        pinturas["tipo"],
                        pinturas["precio"],
                        pinturas["stock"]])
        if not c.exists():
            c.touch()
        with open(c, mode='w', newline='') as stream:
            csv_file = csv.writer(stream)
            for pinturas in data:
                csv_file.writerow(pinturas)
        print('...\nExportación Exitosa!\n')

while True:
    menux(menup)
    ans = respuesta()
    os.system('cls')
    if ans == '1':
        total_stock(rutajson)
    elif ans == '2':
        filtro_pintura(rutajson, buscar_pintura())
    elif ans == '3':
        existe_json(rutajson)
        json_file = leer_json(rutajson)
        data = pedir_datos()
        json_file.append(data)
        cargar_json(rutajson, json_file)
        print('Pintura agregada correctamente!\n')
    elif ans == '4':
        eliminar_pintura(rutajson, pedir_codigo())
        print('...\nPintura eliminada exitosamente\n')
    elif ans == '5':
        exportar(rutajson, archivocsv)
    elif ans == '6':
        exit('Adios chaval')
    else:
        no_válida()

#AZULXFAVOR:C