import numpy as np
import galois
import json
import os
import math

## SUBCONJUNTOS
def get_sets(modulo, num_subsets, GF):
    """Crea el array con todas las posibilidades para los sets y devuelve los que tengan repetidos 3 veces"""
    sets = []

    f = galois.Poly([1,0,0,0], field=GF)
    for i in range(modulo):
        sets.append(f(int(i)))
    count_map = {} # {num: [posiciones]}
    for i, num in enumerate(sets):
        if int(num) in count_map:
            count_map[int(num)].append(int(i))
        else:
            count_map[int(num)] = [int(i)]
    
    result = []
    for num, positions in count_map.items():
        if len(positions) == 3:
            result.append({num: positions[:3]})
        if len(result) >= num_subsets:
            break

    return result

## ENCODER
def encode(n, k, subsets, message, p, GF):
    """Codificador"""
    encoded_msg = []

    # Igualamos el mensaje
    while len(message) % k != 0:
        message.append(0)

    for l in range(0, len(message), k):
        for i in subsets:
            for j in i.values():
                for m in j: # Evalúa cada número de cada set
                    a = message[l:l+k]
                    a00 = a[0]
                    a01 = a[1]
                    a10 = a[2]
                    a11 = a[3]
                    fx = galois.Poly([a00, a01, 0, a10, a11], field=GF)
                    encoded_msg.append(fx(m))
    return encoded_msg

## DECODER
def decode(n, k, encoded_msg, subsets, GF):
    """Decodificador"""
    decoded_msg = []
    
    f1 = galois.Poly([1, 0, 0, 0, 0], field=GF)
    f2 = galois.Poly([0, 1, 0, 0, 0], field=GF)
    f3 = galois.Poly([0, 0, 0, 1, 0], field=GF)
    f4 = galois.Poly([0, 0, 0, 0, 1], field=GF)

    m = []

    ## Posiciones 0, 1, 3 y 6
    ## OJO: Deben coincidir con las decodificadas abajo!!!
    for num in [list(subsets[0].values())[0][0], list(subsets[0].values())[0][1], list(subsets[1].values())[0][0], list(subsets[2].values())[0][0]]:
        row = [f1(num), f2(num), f3(num), f4(num)]
        m.append(row)

    x_data = GF(m)

    for i in range(0, len(encoded_msg), n):
        msg = encoded_msg[i:i+n]
        ## OJO: Deben coincidir con las posiciones de arriba!!
        y_data = GF([msg[0], msg[1], msg[3], msg[6]])

        # Calcular los coeficientes
        A = np.linalg.solve(x_data, y_data)
        decoded_msg += [int(j) for j in A]

    return decoded_msg

## SHARDS
def get_shards(directorio):
    shards = []
    for filename in os.listdir(directorio):
        print(filename)
        if filename.endswith(".shard"):
            shard_path = os.path.join(directorio, filename)
            # Leer el fichero
            with open(shard_path, "rb") as file:
                shards.append(bytearray(file.read()))
    array_recuperado = []
    for shard in shards:
        array_recuperado.extend(shard)
    return array_recuperado


def set_shards(array_codificado, num_shards):
    # Calcula el tamaño aproximado de cada shard
    shard_size = math.ceil(len(array_codificado) / num_shards)
    print(shard_size)
    inicio = 0
    
    directorio_salida = 'shards'
    # Crea el directorio de salida si no existe
    if not os.path.exists(directorio_salida):
        os.makedirs(directorio_salida)
    
    for i in range(num_shards):
        fin = min(inicio + shard_size, len(array_codificado))
        shard = array_codificado[inicio:fin]
        shard_path = os.path.join(directorio_salida, f"shard_{i}.shard")
        # Write the bytes to a file
        with open(shard_path, "wb") as file:
            file.write(bytearray(shard))
        inicio = fin

def check_shards_folder(folder):
    if not os.path.exists(folder):
        print(f"La carpeta {folder} no existe.")
        return
    
    files = os.listdir(folder)
    
    if not files:
        print(f"La carpeta {folder} está vacía.")
        return
    
    for file in files:
        file_route = os.path.join(folder, file)
        try:
            os.remove(file_route)
        except Exception as e:
            print(f"No se pudo eliminar el archivo {file}: {e}")


### MAIN
if __name__ == "__main__":
    p = 256 
    n = 9
    k = 4
    r = 2
    
    GF=galois.GF(p)

    # Conjuntos
    subsets = get_sets(p, n/(r+1), GF)
    print("Sets empleados: %s" % subsets)

    check_shards_folder("shards")

    filename = input("Fichero a codificar: ").strip().lower()

    # Leer el fichero
    with open(filename, "rb") as file:
        message = bytearray(file.read())
    len_msg = len(message)
            
    #print("Mensaje: %s" % message)
    # Codificación
    encoded_msg = encode(n, k, subsets, message, p, GF)
    print("Codificado.")
    set_shards(encoded_msg, n)

    #############################################
    print("Ahora puedes borrar hasta dos shards.")
    input("Pulsa cualquier letra para continuar con la decodificación: ").strip().lower()
    # Decode
    coded_msg = get_shards("shards")
    #TODO: recuperación de errores

    # Decodificación
    decoded_msg = decode(n, k, coded_msg, subsets, GF)
    print("Decodificado.")

    filename = input("Nombre que le quieres dar al fichero recuperado: ").strip().lower()
    
    folder = "decoded"
    if not os.path.exists(folder):
        print(f"La carpeta {folder} no existe. Creando la carpeta...")
        try:
            os.makedirs(folder)
            print(f"Carpeta {folder} creada exitosamente.")
        except Exception as e:
            print(f"No se pudo crear la carpeta {folder}: {e}")
        
    with open(f'{folder}/{filename}', "wb") as archivo:
        write_bytes = bytes(''.join([chr(x) for x in decoded_msg]), encoding="raw_unicode_escape")
        archivo.write(write_bytes[:len_msg])
        print("Se ha almacenado en la carpeta 'decoded'.")

