'''This module DEcodes the original message'''
import zlib 


def three_bit_decoding(s):
  bin_s = bin(int.from_bytes(s, 'big'))[2:]

  # ------
  while len(bin_s) % 8 != 0:
    bin_s = '0' + bin_s
  
  while len(bin_s) % 3 != 0:
    bin_s += '0'
  
  bin_s_dec = ''
  for i in range(len(bin_s)):
    if i % 3 == 0:
      bin_s_dec += str(round((int(bin_s[i]) + int(bin_s[i + 1]) + int(bin_s[i + 2])) / 3)) 
    i += 1

  bin_s_dec += '0' * (((len(bin_s_dec) + 8) - (len(bin_s_dec) + 8) - len(bin_s_dec)) % 8)
  s_dec = int(bin_s_dec, 2)
  return s_dec.to_bytes((s_dec.bit_length() + 7) // 8, 'big')


def read_corrupted_file(s, CHUNKSIZE=1024):
  d = zlib.decompressobj(zlib.MAX_WBITS | 32)
  result_str = b''
  s_chunks = [s[i:i + CHUNKSIZE] for i in range(0, len(s), CHUNKSIZE)]
  try:
    for chunk in s_chunks:
      result_str += d.decompress(chunk)
  except:
    print('FAULT')
    pass
  return result_str


def decoder(filein, fileout, use3bit=True):
  s = filein.read()

  if use3bit:
    s = three_bit_decoding(s)

  chunk_positions = {}
  chunk_i = s.find(b'chunk', 0)
  while chunk_i != -1:
    try:
      chunk_i_num = int(s[chunk_i + 5 : chunk_i + 5 + 4])
    except:
      chunk_i = s.find(b'chunk', chunk_i + 1)
      continue

    if chunk_i_num not in chunk_positions:
      chunk_positions[chunk_i_num] = []
    
    chunk_i_end = s.find(b'CRC', chunk_i) + 3 + 13
    chunk_positions[chunk_i_num].append(s[chunk_i : chunk_i_end])
    
    chunk_i = s.find(b'chunk', chunk_i + 1)
  

  correct_chunks = {}
  for chunk_pos_i in chunk_positions:
    for chunk_copy in chunk_positions[chunk_pos_i]:
      data = chunk_copy[:-13]
      try:
        crc = int(chunk_copy[-13:])
      except:
        # print('except error in', chunk_pos_i)
        continue

      if zlib.crc32(data) == crc:
        correct_chunks[chunk_pos_i] = data[9:-3]
        break #! Можно оставить для наглядных логов
      else:
        # print('error in', chunk_pos_i)
        pass

  sorted_chunk_nums = list(correct_chunks.keys())
  sorted_chunk_nums.sort()
  # print(sorted_chunk_nums)
  # print(len(sorted_chunk_nums))

  compressed = b''
  for i in sorted_chunk_nums:
    compressed += correct_chunks[i]

  decompressed = read_corrupted_file(compressed)

  if len(decompressed) == 0:
    fileout.write('decompressed = 0\n')

  fileout.write(decompressed)
