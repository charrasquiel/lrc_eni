import numpy as np
from sympy import div, symbols, Poly, lcm, solve
import galois

from scipy.optimize import curve_fit


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

def polynomial_function(x, p, a00, a01, a10, a11):
    return (a00*1 + a01*x + a10*x**3 + a11*x**4) % p

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

def decode(n, k, encoded_msg, subsets, GF):
    """Decodificador"""
    decoded_msg = []
    
    p_decod1 = galois.Poly([1, 0, 0, 0, 0], field=GF)
    p_decod2 = galois.Poly([0, 1, 0, 0, 0], field=GF)
    p_decod3 = galois.Poly([0, 0, 0, 1, 0], field=GF)
    p_decod4 = galois.Poly([0, 0, 0, 0, 1], field=GF)

    m = []
    for i in range(4):
        row = [p_decod1(i + 1), p_decod2(i + 1), p_decod3(i + 1), p_decod4(i + 1)]
        m.append(row)

    x_data = GF(m)

    for i in range(0, len(encoded_msg), n):
        msg = encoded_msg[i:i+n]
        y_data = GF([msg[0], msg[3], msg[6], msg[7]])

        # Calcular los coeficientes
        A = np.linalg.solve(x_data, y_data)
        decoded_msg += [int(j) for j in A]

    return decoded_msg

### MAIN
if __name__ == "__main__":
    p = 256 
    n = 9
    k = 4
    r = 2
    
    GF=galois.GF(p)
    #print(GF.properties)

    # Mensaje
    #TODO: cambiar por el fichero leido
    message = [1, 0, 1, 0, 1, 0, 1, 1, 1, 1]
    #print("Mensaje: %s" % message)

    # Conjuntos
    subsets = get_sets(p, n/(r+1), GF)
    print("Sets empleados: %s" % subsets)

    # Codificación
    encoded_msg = encode(n, k, subsets, message, p, GF)
    print("Codificado: %s" % np.array(encoded_msg))

    #TODO: dividir en shards

    # Decodificación
    decoded_msg = decode(n, k, encoded_msg, subsets, GF)
    print("Decodificado: %s" % decoded_msg)


