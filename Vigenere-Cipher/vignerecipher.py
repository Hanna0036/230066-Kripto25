def enkripsi(plaintext, key):
    ciphertext = ""
    key = key.upper()
    key_length = len(key)
    key_as_int = [ord(i) - ord('A') for i in key]
    plaintext_int = [ord(i) - ord('A') for i in plaintext]
    
    for i in range(len(plaintext_int)):
        value = (plaintext_int[i] + key_as_int[i % key_length]) % 26
        ciphertext += chr(value + ord('A'))
    return ciphertext

def dekripsi(ciphertext, key):
    plaintext = ""
    key = key.upper()
    key_length = len(key)
    key_as_int = [ord(i) - ord('A') for i in key]
    ciphertext_int = [ord(i) - ord('A') for i in ciphertext]
    
    for i in range(len(ciphertext_int)):
        value = (ciphertext_int[i] - key_as_int[i % key_length] + 26) % 26
        plaintext += chr(value + ord('A'))
    return plaintext



#MAIN PROGRAM
opsi = input("Pilih menu: (1) Enkripsi (2) Dekripsi: ")

if opsi == "1":
    plaintext = input("Masukkan plaintext (huruf kapital tanpa spasi): ").upper()
    key = input("Masukkan kunci: ").upper()
    ciphertext = enkripsi(plaintext, key)
    print("Ciphertext:", ciphertext)

elif opsi == "2":
    ciphertext = input("Masukkan ciphertext (huruf kapital tanpa spasi): ").upper()
    key = input("Masukkan kunci: ").upper()
    plaintext = dekripsi(ciphertext, key)
    print("Plaintext:", plaintext)

else:
    print("Pilihan tidak valid.")
