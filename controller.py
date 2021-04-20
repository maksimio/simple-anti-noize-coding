'''The controller connects the modules encoder and decoder
 and simulates their real interaction'''
from time import time, sleep
from random import random
from encoder import encoder
from decoder import decoder


def codering(fname_in, fname_out, coder_func, use3bit=True):
  '''Apply coder to fname_in. Out result in fname_out. 
  Coder function is coder_func (encoder or decoder)'''

  with open('test_files/' + fname_in, 'rb') as filein:
    with open('test_files/' + fname_out, 'wb') as fileout:
      start = time()
      coder_func(filein, fileout, use3bit=use3bit)
      print(coder_func.__name__ + ' time:', time() - start)


def make_noize(fname_inout):
  '''Make noise in two ways: 
  1. Loss of block data
  2. Uniform bit noise'''
  noize = 1 # in %

  with open('test_files/' + fname_inout, 'rb') as fileS:
    s = fileS.read()
    print('Byte size input: ', len(s))
    s = s[30000:-10000]
    print('Byte size after loss of block: ', len(s))

    with open('test_files/' + fname_inout, 'wb') as fileS:
      bin_s = bin(int.from_bytes(s, 'big'))[2:]
      bin_s_with_errors = ''
      count_error = 0
      noize /= 100
      for bit in bin_s:
        if random() < noize:
          count_error += 1
          if int(bit):
            bin_s_with_errors += '0'
          else:
            bin_s_with_errors += '1'
        else:
          bin_s_with_errors += bit
      
      s_enc = int(bin_s_with_errors, 2)
      s_enc = s_enc.to_bytes((s_enc.bit_length() + 7) // 8, 'big')
      fileS.write(s_enc)
  print('Errors count: ', count_error)


if __name__ == '__main__':
  use3bit = True
  codering('1_input.dat', '2_encoded.dat', encoder, use3bit=use3bit)
  # make_noize('2_encoded.dat') # You can comment this line for coding without noize
  codering('2_encoded.dat', '3_decoded.dat', decoder, use3bit=use3bit)
