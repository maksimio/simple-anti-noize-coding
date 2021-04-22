'''This module ENcodes the original message'''
import zlib


def three_bit_encoding(s):
  bin_s = bin(int.from_bytes(s, 'big'))[2:]

  bin_s_enc = ''
  for bit in bin_s:
    bin_s_enc += bit * 3

  s_enc = int(bin_s_enc, 2)
  return s_enc.to_bytes((s_enc.bit_length() + 7) // 8, 'big')


def encoder(filein, fileout, use3bit=True):
  # Settings options:
  chunk_size = 100
  s_repeats = 10

  s = filein.read()
  compressed = zlib.compress(s) # In our case on olimpiad the compression was ~tenfold

  chunk_lst = [compressed[i:i + chunk_size] for i in range(0, len(compressed), chunk_size)]

  i, encoded_block = 0, b''
  for chunk in chunk_lst:
    chunk_number = b'chunk' + '{:04d}'.format(i).encode()
    crc_data_block = chunk_number + chunk + b'CRC'
    crc = '{:013d}'.format(zlib.crc32(crc_data_block)).encode()
    encoded_block += crc_data_block + crc
    i += 1
  
  encoded = encoded_block * s_repeats 
  
  if use3bit:
    encoded = three_bit_encoding(encoded)
  
  fileout.write(encoded)