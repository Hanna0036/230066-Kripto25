from PIL import Image

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary):
    if len(binary) % 8 != 0:
        binary = binary[:-(len(binary) % 8)]

    text = ""
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if '1' not in byte and len(byte) == 8:
             break
        text += chr(int(byte, 2))
    return text

def encode(image_path, secret_message, output_path):
    try:
        img = Image.open(image_path)
        secret_message += "#####" 
        binary_message = text_to_binary(secret_message)
        
        if len(binary_message) > img.width * img.height * 3:
            raise ValueError("Pesan terlalu panjang untuk gambar ini!")

        data_index = 0
        img_data = iter(img.getdata())

        new_pixels = []
        for pixel in img_data:
            new_pixel = list(pixel)
            for i in range(3):
                if data_index < len(binary_message):
                    new_pixel[i] = int(format(pixel[i], '08b')[:-1] + binary_message[data_index], 2)
                    data_index += 1
                else:
                    break
            new_pixels.append(tuple(new_pixel))

        while True:
            try:
                new_pixels.append(next(img_data))
            except StopIteration:
                break

        encoded_img = Image.new(img.mode, img.size)
        encoded_img.putdata(new_pixels)
        encoded_img.save(output_path, "PNG")
        print(f"Pesan berhasil disembunyikan di '{output_path}'")

    except FileNotFoundError:
        print(f"Error: File '{image_path}' tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")


def decode(stego_image_path):
    try:
        img = Image.open(stego_image_path)
        binary_data = ""
        for pixel in img.getdata():
            for value in pixel[:3]:
                binary_data += format(value, '08b')[-1]

        all_bytes = [binary_data[i: i+8] for i in range(0, len(binary_data), 8)]
        decoded_message = ""
        for byte in all_bytes:
            decoded_message += chr(int(byte, 2))
            if decoded_message[-5:] == "#####":
                print("🔍 Pesan ditemukan!")
                return decoded_message[:-5]
        
        print("Tidak ada pesan tersembunyi yang ditemukan.")
        return None

    except FileNotFoundError:
        print(f"Error: File '{stego_image_path}' tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan saat decode: {e}")

if __name__ == "__main__":
    mode = input("Pilih mode ('encode' atau 'decode'): ").lower()
    if mode == 'encode':
        cover_image = input("Masukkan nama file gambar (e.g., cover.png): ")
        message = input("Masukkan pesan rahasia: ")
        output_image = input("Masukkan nama file output (e.g., stego.png): ")
        encode(cover_image, message, output_image)
    
    elif mode == 'decode':
        stego_image = input("Masukkan nama file gambar yang ada pesannya (e.g., stego.png): ")
        secret_text = decode(stego_image)
        if secret_text:
            print("-----------------------------------")
            print("Pesan Rahasianya adalah:")
            print(secret_text)
            print("-----------------------------------")
    else:
        print("Mode tidak valid. Silakan pilih 'encode' atau 'decode'.")