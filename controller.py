from time import time, sleep
from random import random
from encoder import encoder
from decoder import decoder


def codering(fname_in, fname_out, coder_func):
  '''Apply coder to fname_in. Out in fname_out. 
  Coder function is coder_func (encoder or decoder)'''

  with open('test_files/' + fname_in, 'rb') as filein:
    with open('test_files/' + fname_out, 'wb') as fileout:
      start = time()
      coder_func(filein, fileout)
      print(coder_func.__name__ + ' time:', time() - start)


def make_noize(fname_inout):
  '''Make noise in two'''
  with open('test_files/' + fname_inout, 'rb') as fileS:
    s = fileS.read()
    print(len(s))
    # s = s[:len(s) - 1000000] + b'u'*499999 + s[len(s) - 500000:]
    # s = s[:-2]
    print(len(s))

    with open('test_files/' + fname_inout, 'wb') as fileS:
      bin_s = bin(int.from_bytes(s, 'big'))[2:]
      bin_s_with_errors = ''
      count_error = 0
      for bit in bin_s:
        if random() < 0.01:
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
  codering('1_input.dat', '2_encoded.dat', encoder)
  make_noize('2_encoded.dat')
  codering('2_encoded.dat', '3_decoded.dat', decoder)
