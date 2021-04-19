import zlib


def three_bit_encoding(s):
  bin_s = bin(int.from_bytes(s, 'big'))[2:]

  # ------ Шифровка
  bin_s_enc = ''
  for bit in bin_s:
    if bit == '1':
      bin_s_enc += '111'
    elif bit == '0':
      bin_s_enc += '000'
  # ------

  s_enc = int(bin_s_enc, 2)
  return s_enc.to_bytes((s_enc.bit_length() + 7) // 8, 'big')


def encoder(filein, fileout):
  s = filein.read()
  compressed = zlib.compress(s)
  # --- --- Делаем сообщение помехоустойчивым:
  chunksize = 100 # 200
  blockcount = 10  # 9
  chunk_lst = [compressed[i:i + chunksize] for i in range(0, len(compressed), chunksize)]

  i = 0
  encoded_block = b''
  for chunk in chunk_lst:
    chunknumber = b'chunk' + '{:04d}'.format(i).encode()
    crc_data_block = chunknumber + chunk + b'CRC'
    crc = '{:013d}'.format(zlib.crc32(crc_data_block)).encode()
    encoded_block += crc_data_block + crc
    i += 1
  
  encoded = encoded_block * blockcount
  
  #* Здесь нужно троебитное кодирование encoded
  encoded = three_bit_encoding(encoded)
  
  fileout.write(encoded)