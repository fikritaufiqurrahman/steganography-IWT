import random

CHUNK_LENGTH = 8

assert not CHUNK_LENGTH % 8, 'Panjang blok harus kelipatan 8'

CHECK_BITS = [i for i in range(1, CHUNK_LENGTH + 1) if not i & (i - 1)]


def chars_to_bin(chars):
    """
    Konversi karakter ke format biner
    """
    assert not len(chars) * 8 % CHUNK_LENGTH, 'Panjang data yang disandikan harus merupakan kelipatan dari panjang blok penyandian'
    return ''.join([bin(ord(c))[2:].zfill(8) for c in chars])


def chunk_iterator(text_bin, chunk_size=CHUNK_LENGTH):
    """
    Pemrosesan Blok untuk Menampilkan Data Biner
    """
    for i in range(len(text_bin)):
        if not i % chunk_size:
            yield text_bin[i:i + chunk_size]


def get_check_bits_data(value_bin):
    """
    Mendapatkan informasi tentang bit kontrol dari blok data biner
    """
    check_bits_count_map = {k: 0 for k in CHECK_BITS}
    for index, value in enumerate(value_bin, 1):
        if int(value):
            bin_char_list = list(bin(index)[2:].zfill(8))
            bin_char_list.reverse()
            for degree in [2 ** int(i) for i, value in enumerate(bin_char_list) if int(value)]:
                check_bits_count_map[degree] += 1
    check_bits_value_map = {}
    for check_bit, count in check_bits_count_map.items():
        check_bits_value_map[check_bit] = 0 if not count % 2 else 1
    return check_bits_value_map


def set_empty_check_bits(value_bin):
    """
    Menambahkan bit kontrol "kosong" ke dalam blok biner.
    """
    for bit in CHECK_BITS:
        value_bin = value_bin[:bit - 1] + '0' + value_bin[bit - 1:]
    return value_bin


def set_check_bits(value_bin):
    """
    Mengatur Nilai Bit Kontrol
    """
    value_bin = set_empty_check_bits(value_bin)
    check_bits_data = get_check_bits_data(value_bin)
    for check_bit, bit_value in check_bits_data.items():
        value_bin = '{0}{1}{2}'.format(
            value_bin[:check_bit - 1], bit_value, value_bin[check_bit:])
    return value_bin


def get_check_bits(value_bin):
    """
    Untuk mendapatkan informasi tentang bit kontrol dari blok data biner
    """
    check_bits = {}
    for index, value in enumerate(value_bin, 1):
        if index in CHECK_BITS:
            check_bits[index] = int(value)
    return check_bits


def exclude_check_bits(value_bin):
    """
    Menghilangkan informasi bit kontrol dari blok data biner
    """
    clean_value_bin = ''
    for index, char_bin in enumerate(list(value_bin), 1):
        if index not in CHECK_BITS:
            clean_value_bin += char_bin

    return clean_value_bin


def set_errors(encoded):
    """
    Mengizinkan kesalahan dalam blok-blok data biner
    """
    result = ''
    for chunk in chunk_iterator(encoded, CHUNK_LENGTH + len(CHECK_BITS)):
        num_bit = random.randint(1, len(chunk))
        chunk = '{0}{1}{2}'.format(chunk[:num_bit - 1], int(chunk[num_bit - 1]) ^ 1, chunk[num_bit:])
        result += (chunk)
    return result


def check_and_fix_error(encoded_chunk):
    #print("encoded_chunk = ", encoded_chunk)
    """
    Pemeriksaan dan Perbaikan Kesalahan dalam Blok Data Biner
    """
    check_bits_encoded = get_check_bits(encoded_chunk)
    check_item = exclude_check_bits(encoded_chunk)
    check_item = set_check_bits(check_item)
    check_bits = get_check_bits(check_item)
    if check_bits_encoded != check_bits:
        invalid_bits = []
        for check_bit_encoded, value in check_bits_encoded.items():
            if check_bits[check_bit_encoded] != value:
                invalid_bits.append(check_bit_encoded)
        #num_bit = sum(invalid_bits)
        num_bit = invalid_bits[0]
        #print("number_bits_with_error = ", num_bit)
        encoded_chunk = '{0}{1}{2}'.format(
            encoded_chunk[:num_bit - 1],
            int(encoded_chunk[num_bit - 1]) ^ 1,
            encoded_chunk[num_bit:])
    return encoded_chunk


def get_diff_index_list(value_bin1, value_bin2):
    """
    Untuk mendapatkan daftar indeks bit yang berbeda antara dua bilangan
    """
    diff_index_list = []
    for index, char_bin_items in enumerate(zip(list(value_bin1), list(value_bin2)), 1):
        if char_bin_items[0] != char_bin_items[1]:
            diff_index_list.append(index)
    return diff_index_list


def encode(source):
    """
    Pencocokan data
    """
    text_bin = chars_to_bin(source)
    result = ''
    for chunk_bin in chunk_iterator(text_bin):
        chunk_bin = set_check_bits(chunk_bin)
        result += chunk_bin
    return result

def encode_my(text_bin):
    """
    Data encoding 
    """
    result = ''
    for chunk_bin in chunk_iterator(text_bin):
        chunk_bin = set_check_bits(chunk_bin)
        result += chunk_bin
    return result

def decode(encoded, fix_errors=True):
    """
    Dekode data
    """
    decoded_value = ''
    fixed_encoded_list = []
    for encoded_chunk in chunk_iterator(encoded, CHUNK_LENGTH + len(CHECK_BITS)):
        if fix_errors:
            encoded_chunk = check_and_fix_error(encoded_chunk)
        fixed_encoded_list.append(encoded_chunk)

    clean_chunk_list = []
    for encoded_chunk in fixed_encoded_list:
        encoded_chunk = exclude_check_bits(encoded_chunk)
        clean_chunk_list.append(encoded_chunk)

    print("clean_chunk_list = ", clean_chunk_list)

    for clean_chunk in clean_chunk_list:
        for clean_char in [clean_chunk[i:i + 8] for i in range(len(clean_chunk)) if not i % 8]:
            decoded_value += chr(int(clean_char, 2))
    return decoded_value


def decode_my(encoded, fix_errors=True):
    """
    Dekode data
    """
    decoded_value = ''
    fixed_encoded_list = []
    for encoded_chunk in chunk_iterator(encoded, CHUNK_LENGTH + len(CHECK_BITS)):
        if fix_errors:
            encoded_chunk = check_and_fix_error(encoded_chunk)
        fixed_encoded_list.append(encoded_chunk)

    clean_chunk_list = []
    for encoded_chunk in fixed_encoded_list:
        encoded_chunk = exclude_check_bits(encoded_chunk)
        clean_chunk_list.append(encoded_chunk)

    return clean_chunk_list



if __name__ == '__main__':
    source = input('Tentukan teks yang akan dikodekan/didekodekan:')
    print('Panjang blok pengkodean: {0}'.format(CHUNK_LENGTH))
    print('Bit kontrol: {0}'.format(CHECK_BITS))
    encoded = encode(source)
    print('Data yang dikodekan: {0}'.format(encoded))
    decoded = decode(encoded)
    print('Hasil decoding: {0}'.format(decoded))
    encoded_with_error = set_errors(encoded)
    print('Kami mengizinkan kesalahan dalam data yang dikodekan: {0}'.format(encoded_with_error))
    diff_index_list = get_diff_index_list(encoded, encoded_with_error)
    print('Terjadi kesalahan dalam bit-bit yang dikodekan: {0}'.format(diff_index_list))
    decoded = decode(encoded_with_error, fix_errors=False)
    print('Hasil decoding data yang salah tanpa koreksi kesalahan: {0}'.format(decoded))
    decoded = decode(encoded_with_error)
    print('Hasil decoding data yang salah dengan koreksi kesalahan: {0}'.format(decoded))
