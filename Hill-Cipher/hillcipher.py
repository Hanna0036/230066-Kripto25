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
def convertTeks(angka):
    return ''.join(huruf[n] for n in angka)

# cari invers dari sebuah bilangan mod 26
def modInverse(a, m=26):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

# Inverse Matrix 2x2
def inverseMatriksKunci(matrix):
    a, b = matrix[0]
    c, d = matrix[1]

    det = (a*d - b*c) % 26
    det_inv = modInverse(det, 26)
    if det_inv is None:
        raise ValueError("Matriks kunci tidak punya invers mod 26")

    adj = [[d, -b],
           [-c, a]]

    inv_matrix = [[(det_inv * adj[i][j]) % 26 for j in range(2)] for i in range(2)]
    return inv_matrix

# fungsi enkripsi
def hillEncrypt(plaintext, matriksKunci):
    angka_plain = convert(plaintext)
    if len(angka_plain) % 2 != 0:
        angka_plain.append(huruf.index('x'))  

    hasil = []
    for i in range(0, len(angka_plain), 2):
        p1, p2 = angka_plain[i], angka_plain[i+1]
        c1 = (matriksKunci[0][0]*p1 + matriksKunci[0][1]*p2) % 26
        c2 = (matriksKunci[1][0]*p1 + matriksKunci[1][1]*p2) % 26
        hasil.extend([c1, c2])
    return hasil

# fungsi dekripsi
def hillDecrypt(cipher_numbers, matriksKunci):
    inv_matrix = inverseMatriksKunci(matriksKunci)

    hasil = []
    for i in range(0, len(cipher_numbers), 2):
        c1, c2 = cipher_numbers[i], cipher_numbers[i+1]
        p1 = (inv_matrix[0][0]*c1 + inv_matrix[0][1]*c2) % 26
        p2 = (inv_matrix[1][0]*c1 + inv_matrix[1][1]*c2) % 26
        hasil.extend([p1, p2])
    return hasil

# fungsi untuk mencari kunci Hill Cipher
def cariKunciHill(plaintext, ciphertext):
    try:
        # Konversi ke angka
        plain_numbers = convert(plaintext)
        cipher_numbers = convert(ciphertext)
        
        # Pastikan panjang sama dan genap
        if len(plain_numbers) != len(cipher_numbers):
            raise ValueError("Panjang plaintext dan ciphertext harus sama!")
        
        if len(plain_numbers) < 4:
            raise ValueError("Minimal diperlukan 4 karakter (2 blok) untuk mencari kunci 2x2!")
        
        # Ambil 2 blok pertama (4 karakter)
        # Blok pertama
        p1, p2 = plain_numbers[0], plain_numbers[1]
        c1, c2 = cipher_numbers[0], cipher_numbers[1]
        
        # Blok kedua  
        p3, p4 = plain_numbers[2], plain_numbers[3]
        c3, c4 = cipher_numbers[2], cipher_numbers[3]
        
        # Buat matriks plaintext P = [[p1, p3], [p2, p4]]
        P = [[p1, p3], [p2, p4]]
        
        # Buat matriks ciphertext C = [[c1, c3], [c2, c4]]
        C = [[c1, c3], [c2, c4]]
        
        # Hitung invers dari matriks P
        try:
            P_inv = inverseMatriksKunci(P)
        except ValueError:
            raise ValueError("Matriks plaintext tidak dapat diinvers! Coba dengan plaintext yang berbeda.")
        
        # Hitung K = C * P_inv (mod 26)
        K = [[0, 0], [0, 0]]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    K[i][j] = (K[i][j] + C[i][k] * P_inv[k][j]) % 26
        
        # Menvalidasi dengan mengenkripsi plaintext menggunakan kunci yang ditemukan
        test_cipher = hillEncrypt(plaintext, K)
        if test_cipher == cipher_numbers:
            return K
        else:
            raise ValueError("Kunci yang ditemukan tidak valid! Periksa input plaintext dan ciphertext.")
            
    except Exception as e:
        raise ValueError(f"Error dalam pencarian kunci: {str(e)}")

# input matriks kunci manual
def inputMatriksKunci():
    matriksKunci = []
    print("Masukkan elemen matriks kunci 2x2 (baris per baris):")
    for i in range(2):
        baris = []
        for j in range(2):
            elemen = int(input(f"Elemen [{i+1},{j+1}]: "))
            baris.append(elemen)
        matriksKunci.append(baris)
    return matriksKunci

# fungsi untuk menampilkan matriks
def tampilkanMatriks(matrix):
    print("Matriks kunci:")
    for baris in matrix:
        print(f"[{baris[0]:2d} {baris[1]:2d}]")

# MENU
while True:
    print("\n=== HILL CIPHER ===")
    print("1. Enkripsi")
    print("2. Dekripsi")
    print("3. Cari Kunci Hill Cipher")
    print("4. Keluar")
    pilih = input("Pilih menu: ")

    if pilih == "1":
        plain = input("Masukkan plaintext: ")
        kunci = inputMatriksKunci()
        cipher_numbers = hillEncrypt(plain, kunci)
        cipher_text = convertTeks(cipher_numbers)
        print("Ciphertext:", cipher_text)

    elif pilih == "2":
        cipher = input("Masukkan ciphertext: ")
        cipher_numbers = convert(cipher)
        kunci = inputMatriksKunci()
        decrypted_numbers = hillDecrypt(cipher_numbers, kunci)
        decrypted_text = convertTeks(decrypted_numbers)
        print("Plaintext:", decrypted_text)

    elif pilih == "3":
        print("\n=== NYARI KUNCI HILL CIPHER ===")
        print("Catatan: Harus ada minimal ciphertext(4 karakter) dan plaintext(4 karakter) ")
        plaintext = input("Masukkan plaintext yang diketahui: ")
        ciphertext = input("Masukkan ciphertext yang diketahui: ")
        
        try:
            kunci = cariKunciHill(plaintext, ciphertext)
            print("\nKunci Hill Cipher berhasil ditemukan!")
            tampilkanMatriks(kunci)
            
            # Verifikasi dengan mengenkripsi plaintext
            test_cipher = hillEncrypt(plaintext, kunci)
            test_cipher_text = convertTeks(test_cipher)
            print(f"\nVerifikasi:")
            print(f"Plaintext input : {plaintext}")
            print(f"Ciphertext asli : {ciphertext}")
            print(f"Ciphertext test : {test_cipher_text}")
            print(f"Status: {'COCOK' if test_cipher_text.lower() == ciphertext.lower() else 'TIDAK COCOK'}")
            
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

    elif pilih == "4":
        print("Keluar...")
        break

    else:
        print("Pilihan tidak valid!")