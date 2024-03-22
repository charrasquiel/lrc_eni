import numpy as np
import galois
from tqdm import tqdm
import time
import os
import csv


## SUBCONJUNTOS
def get_sets(modulo, num_subsets, GF):
    """Crea el array con todas las posibilidades para los sets y devuelve los que tengan repetidos 3 veces"""
    sets = []

    f = galois.Poly([1,0,0,0], field=GF)
    for i in tqdm(range(modulo)):
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
    shards = {}

    # Igualamos el mensaje
    while len(message) % k != 0:
        message.append(0)
    print("Codificando...")
    for l in tqdm(range(0, len(message), k)):
        for i in subsets:
            for j in i.values():
                for index, m in enumerate(j): # Evalúa cada número de cada set
                    a = message[l:l+k]
                    a00 = a[0]
                    a01 = a[1]
                    a10 = a[2]
                    a11 = a[3]
                    fx = galois.Poly([a00, a01, 0, a10, a11], field=GF)
                    if m not in shards:
                        shards[m] = [fx(m)]  
                    else:
                        shards[m].append(fx(m))
    return encoded_msg, shards

## DECODER
def decode(n, k, encoded_msg, subsets, GF):
    """Decodificador"""
    decoded_msg = []
    
    fd = [galois.Poly([1, 0, 0, 0, 0], field=GF),
        galois.Poly([0, 1, 0, 0, 0], field=GF),
        galois.Poly([0, 0, 0, 1, 0], field=GF),
        galois.Poly([0, 0, 0, 0, 1], field=GF)]

    m = []

    ## Posiciones 0, 1, 3 y 6, por ejemplo, podrían variar
    ## OJO: Deben coincidir con las decodificadas abajo!!!
    for num in [list(subsets[0].values())[0][0], list(subsets[0].values())[0][1], list(subsets[1].values())[0][0], list(subsets[2].values())[0][0]]:
        row = [fd[0](num), fd[1](num), fd[2](num), fd[3](num)]
        m.append(row)

    x_data = GF(m)
    print("Decodificando...")
    for i in tqdm(range(0, len(encoded_msg), n)):
        msg = encoded_msg[i:i+n]

        ## OJO: Deben coincidir con las posiciones de arriba!!
        y_data = GF([msg[0], msg[1], msg[3], msg[6]])
        # Calcular los coeficientes
        A = np.linalg.solve(x_data, y_data)
        decoded_msg += [int(j) for j in A]

    return decoded_msg

## RECOVERY
def recover(n, k, subsets, GF, pos, readed_msg):
    recovered_shard = []
    x_recover = []
    y_first = []
    y_second = []

    ## Según el shard borrado cuáles se necesitan para recuperar
    related_pos = {0: [1, 2, 0], 1: [0, 2, 0], 2: [0, 1, 0],
                3: [4, 5, 1], 4: [3, 5, 1], 5: [3, 4, 1],
                6: [7, 8, 2], 7: [6, 8, 2], 8: [6, 7, 2]}
    

    evaluate_in = related_pos.get(pos)
    recov_pos = list(subsets[int(evaluate_in[2])].values())[0]
    x_recover.append([recov_pos[evaluate_in[0]%3],1])
    x_recover.append([recov_pos[evaluate_in[1]%3],1])
    x_data = GF(x_recover)

    y_first.extend(readed_msg[evaluate_in[0]])
    y_second.extend(readed_msg[evaluate_in[1]])

    ## Evaluamos con los dos resultados que tenemos, sacamos los valores A y B y resolvemos
    for i, number in enumerate(y_first):
        y_data = GF([y_first[i], y_second[i]])

        AB = np.linalg.solve(x_data, y_data)
        fd = galois.Poly(AB, field=GF)
        sol = fd(recov_pos[pos%3])
        recovered_shard.append(int(sol))
    return recovered_shard

def get_message(n, k, subsets, GF):
    ordered_msg = []
    full_msg = []
    readed_msg, ereased_shards = get_shards("shards")
    coded_msg = []
    ## Conseguir el mensaje primero para poder recuperar los borrados
    print("Recuperando borrados...")
    for i in tqdm(range(0, 9, 1)):
        if i in ereased_shards:
            coded_msg.append([i])
        else:
            coded_msg.append(readed_msg[i])
    
    ## Recuperar y conseguir el mensaje general
    print("Recuperando mensaje original...")
    for m in tqdm(range(0, 9, 1)):
        if m in ereased_shards:
            full_msg.extend(recover(n, k, subsets, GF, m, readed_msg))
        else:
            full_msg.extend(coded_msg[m])

    ## Se leen los shards ordenados con lo que ahora hay que organizarlos para la decodificación
    print("Ordenando datos...")
    for k in tqdm(range(int(len(full_msg)/n))):
        for i in range(0, len(full_msg), int(len(full_msg)/n)):
            ordered_msg.append(full_msg[i+k])
        
    return ordered_msg, len(ereased_shards)


## SHARDS FUNCTIONS
def get_shards(directorio):
    shards = []
    ereased = []
    print("Recuperando datos...")
    for i in tqdm(range(0, 9, 1)):
        filename = f'shard_{i}.shard'
        shards.append([i])
        shard_path = os.path.join(directorio, filename)
        if os.path.exists(shard_path):
            # Leer el fichero
            with open(shard_path, "rb") as file:
                shards[i] = bytearray(file.read())
        else:
            ereased.append(i)
    return shards, ereased


def set_shards(coded_shards):
    directorio_salida = 'shards'
    # Crea el directorio de salida si no existe
    if not os.path.exists(directorio_salida):
        os.makedirs(directorio_salida)
    
    for i, key in enumerate(coded_shards.keys()):
        shard_path = os.path.join(directorio_salida, f"shard_{i}.shard")
        # Write the bytes to a file
        with open(shard_path, "wb") as file:
            file.write(bytearray(coded_shards[key]))

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



# ESCRIBIR MEDIDAS  
def write_to_csv(data):
    with open("data.csv", mode='a', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow(data)

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
    readed = False
    while readed != True:
        filename = input("> Fichero a codificar: ").strip().lower()
        try:
            # Leer el fichero
            with open(filename, "rb") as file:
                message = bytearray(file.read())
                readed = True
        except:
            print("No existe ese fichero.")

    len_msg = len(message) # se necesita para que al recuperar no sobren bits que se pudieron añadir al codificar

    # Codificación
    start_t = time.time()
    encoded_msg, shards = encode(n, k, subsets, message, p, GF)
    end_t = time.time()
    print("Fichero codificado.")
    coded_t = end_t - start_t
    print("Tiempo de codificación: %s" % (end_t - start_t))
    set_shards(shards)

    print("Ahora puedes borrar shards.")
    input("> Introduce cualquier letra para continuar con la decodificación: ").strip().lower()
    # Recuperación del mensaje
    start_t = time.time()
    coded_msg, len_ereased = get_message(n, k, subsets, GF)
    end_t = time.time()
    recovered_t = end_t - start_t
    print("Tiempo de recuperación: %s" % (end_t - start_t))

    # Decodificación
    start_t = time.time()
    decoded_msg = decode(n, k, coded_msg, subsets, GF)
    end_t = time.time()
    decoded_t = end_t - start_t
    print("Fichero decodificado.")
    print("Tiempo de decodificación: %s" % (end_t - start_t))

    #['Longitud del fichero', 'Tiempo de Codificación', 'Tiempo de Recuperación', 'Tiempo de Decodificación', 'Cantidad de shards borrados'])
    write_to_csv([len_msg, coded_t, recovered_t, decoded_t, len_ereased])

    # Reubicación del nuevo fichero decodificado
    filename = input("> Nombre que le quieres dar al fichero recuperado: ").strip().lower()
    
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
        print(f"Se ha almacenado el fichero '{filename}' en la carpeta 'decoded'.")

