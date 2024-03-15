import reedsolomon
# Configuration of the parameters and input message
prim = 0x11d
n = 9 # set the size you want, it must be > k, the remaining n-k symbols will be the ECC code (more is better)
k = 4 # k = len(message)

confirmacion = input("Ingresa fichero para continuar: ")
filename = confirmacion
with open(filename, "rb") as file:
        message = file.read()
#f = open(filename, "r")
#message = f # input message

#print(message)

# Initializing the log/antilog tables
reedsolomon.init_tables(prim)

# Encoding the input message
mesecc = reedsolomon.rs_encode_msg(message, n-k)
#print("Original: %s" % mesecc)

reedsolomon.divide_en_shards(mesecc, n)
confirmacion = input("Ingrese cualquier cosa para continuar: ")
messec = reedsolomon.recuperar_array('shards')

# Decoding/repairing the corrupted message, by providing the locations of a few erasures, we get below the Singleton Bound
# Remember that the Singleton Bound is: 2*e+v <= (n-k)
corrected_message, corrected_ecc = reedsolomon.rs_correct_msg(mesecc, n-k, erase_pos=[0, 1, 2])
#print("Repaired: %s" % (corrected_message+corrected_ecc))
#print("Mensaje reparado: ",''.join([chr(x) for x in corrected_message]))
with open('recovered_'+filename, "wb") as archivo:
    archivo.write(bytes(''.join([chr(x) for x in corrected_message]), encoding="raw_unicode_escape"))