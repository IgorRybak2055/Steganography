from PIL import Image as Img


def encrypt_img(msg, map_of_pixels, pic_width, pic_height):
    w, h = 0, 0

    for i in range(0, len(msg), 6):
        blocks = [msg[i:i+2], msg[i+2:i+4], msg[i+4:i+6]]
        rgb_pixel = list(map_of_pixels[w, h])

        for n in range(3):
            if len(blocks[n]) == 0:
                break

            bin_rgb = list(bin(rgb_pixel[n]).replace('b', ''))
            bin_rgb[-2], bin_rgb[-1] = blocks[n][0], blocks[n][1]
            rgb_pixel[n] = int(''.join(bin_rgb), 2)

        map_of_pixels[w, h] = tuple(rgb_pixel)

        if w == pic_width - 1 and h == pic_height - 1:
            return
        elif w == pic_width - 1:
            h += 1
            w = 0
        else:
            w += 1


def decrypt_img(map_of_pixels, pic_width, pic_height):
    out = ''
    count = 0
    tmp_list = []

    for h in range(pic_height):
        for w in range(pic_width):
            rgb_pixel = map_of_pixels[w, h]

            for n in range(3):
                color_component = rgb_pixel[n]

                if count == 4:
                    symbol = get_litter(tmp_list)

                    if symbol == '&':
                        return out
                    else:
                        out += symbol

                    count, tmp_list = 0, []

                bin_str = bin(color_component).replace('b', '')
                tmp_list.append(bin_str[-2])
                tmp_list.append(bin_str[-1])

                count += 1

    return out


def get_litter(bin_list):
    bin_str = ''.join(bin_list)

    return bytes.fromhex(hex(int(bin_str, 2))[2:]).decode(encoding='ascii')


def encrypt(msg, path):
    img = Img.open(path)
    map_of_pixels = img.load()

    encrypt_img(msg, map_of_pixels, img.size[0], img.size[1])

    img.save('PictureWithMessage.bmp')



def decrypt(path):
    img = Img.open(path)
    pixel_map = img.load()

    return decrypt_img(pixel_map, img.size[0], img.size[1])


if __name__ == '__main__':
    # message = input('Enter message: ') + '&'
    # b_message = bin(int.from_bytes(message.encode(), 'big')).replace('b', '')
    #
    # encrypt(b_message, 'lab6.bmp')
    decrypted_message = decrypt('PictureWithMessage.bmp')

    print('Decrypt message:', decrypted_message)
