def teksKeAngka(text):
    return [ord(ch) - ord('A') for ch in text]

def angkaKeTeks(numbers):
    return ''.join(chr(n + ord('A')) for n in numbers)

def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def enkripsi(plaintext, p, g, x, k):
    y = pow(g, x, p)

    m_list = teksKeAngka(plaintext)

    a = pow(g, k, p)
    yk = pow(y, k, p)

    b_list = [(m * yk) % p for m in m_list]

    return a, b_list

def dekripsi(a, b_list, p, x):
    s = pow(a, x, p)
    s_inv = mod_inverse(s, p)
    m_list = [(b * s_inv) % p for b in b_list]
    return angkaKeTeks(m_list)


# ==== MAIN ====
plaintext = input("Masukkan plaintext (huruf kapital tanpa spasi): ").upper()
p = int(input("Masukkan bilangan prima p: "))
g = int(input("Masukkan generator g: "))
x = int(input("Masukkan kunci privat x: "))
k = int(input("Masukkan k (acak, 1 < k < p-1): "))

print("\n=== ENKRIPSI ===")
a, b_list = enkripsi(plaintext, p, g, x, k)
print("Ciphertext (a,b):")
for b in b_list:
    print(f"({a},{b})", end=" ")
print()

print("\n=== DEKRIPSI ===")
decrypted = dekripsi(a, b_list, p, x)
print("Hasil dekripsi:", decrypted)
