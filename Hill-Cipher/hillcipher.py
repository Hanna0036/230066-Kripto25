huruf = [
 'a', 'b', 'c', 'd', 'e', 'f',
 'g', 'h', 'i', 'j', 'k', 'l',
 'm', 'n', 'o', 'p', 'q', 'r',
 's', 't', 'u', 'v', 'w', 'x',
 'y', 'z'
]

# konversi huruf ke angka
def convert(inputHuruf): 
    convertHuruf = [] 
    for x in range(len(inputHuruf)):
        for y in range(len(huruf)) : 
            if huruf[y] == inputHuruf[x].lower() : 
                convertHuruf.append(y)
                break
    return convertHuruf

# konversi angka ke huruf
def toText(numbers):
    return ''.join(huruf[n] for n in numbers)

# cari invers dari sebuah bilangan mod 26
def modInverse(a, m=26):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None  # kalau gak ada invers

# hitung invers matriks 2x2 mod 26
def inverseKeyMatrix(matrix):
    a, b = matrix[0]
    c, d = matrix[1]

    # determinan
    det = (a*d - b*c) % 26

    # cari invers determinan
    det_inv = modInverse(det, 26)
    if det_inv is None:
        raise ValueError("Matriks kunci tidak punya invers mod 26")

    # matriks adjoint (tukar a<->d, ubah tanda b & c)
    adj = [[d, -b],
           [-c, a]]

    # kalikan dengan invers determinan mod 26
    inv_matrix = [[(det_inv * adj[i][j]) % 26 for j in range(2)] for i in range(2)]

    return inv_matrix

# fungsi enkripsi
def hillEncrypt(plaintext, matriksKunci):
    angka_plain = convert(plaintext)
    if len(angka_plain) % 2 != 0:
        angka_plain.append(huruf.index('x'))  # padding kalau ganjil

    hasil = []
    for i in range(0, len(angka_plain), 2):
        p1, p2 = angka_plain[i], angka_plain[i+1]
        c1 = (matriksKunci[0][0]*p1 + matriksKunci[0][1]*p2) % 26
        c2 = (matriksKunci[1][0]*p1 + matriksKunci[1][1]*p2) % 26
        hasil.extend([c1, c2])
    return hasil

# fungsi dekripsi
def hillDecrypt(cipher_numbers, matriksKunci):
    inv_matrix = inverseKeyMatrix(matriksKunci)

    hasil = []
    for i in range(0, len(cipher_numbers), 2):
        c1, c2 = cipher_numbers[i], cipher_numbers[i+1]
        p1 = (inv_matrix[0][0]*c1 + inv_matrix[0][1]*c2) % 26
        p2 = (inv_matrix[1][0]*c1 + inv_matrix[1][1]*c2) % 26
        hasil.extend([p1, p2])
    return hasil

# contoh
matriksKunci = [[3, 3],
                [2, 5]]

plain = "HELLO"
print("Plaintext :", plain)

cipher_numbers = hillEncrypt(plain, matriksKunci)
cipher_text = toText(cipher_numbers)
print("Ciphertext:", cipher_text)

decrypted_numbers = hillDecrypt(cipher_numbers, matriksKunci)
decrypted_text = toText(decrypted_numbers)
print("Decrypt   :", decrypted_text)
