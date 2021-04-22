# Noiseless coding
This repository contains a set of encoder and decoder that redundantly encode and decode a message. The encoded message is obtained resistant to two types of distortion:

1. Uniform bit noise up to 1%
2. Loss of significant message blocks

## Project structure
The two files _encoder.py_ and _decoder.py_ contain, respectively, only the encoder and decoder code. They are controlled, that is, the cycle of encoding-decoding, is carried out by the _controller.py_. This controller also simulates the distortion of the encoded transfer file.

### Encoding way
Algoritm of encoding: 

1. Compress input file (with zlib)
1. Split compressed file into chunks and add checksum and sequence number to each chunk
1. Duplicate this binary string multiple times
1. Apply three bit encoding

### Decoding way
The decoding algorithm is the opposite of the encoding algorithm. However, we wrote a special function _read_corrupted_file_ that allows you to unpack even a damaged archive at least partially.

Here we are trying to find one intact chunk with CRC32 and place them in order to unzip the message.

## Three bit coding
Сoding each bit with three allows at the decoding stage to correct single bit errors in each bit-triple. Its implementation slows down the program hundreds of times.

## Why is compression using
The use of such an algorithm was an attempt (unsuccessful) to earn points in the distance NTI Olympiad (Russia).

Something went wrong, the message was not transmitted. Our team still doesn't understand why it didn't work. But I find this code worthy of being here.

> In NTI Olympiad, the source file had the content as file _1_input.dat_. Therefore, the compression in our case was effective.