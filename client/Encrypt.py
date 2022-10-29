from encodings import utf_8
import sys
import operator
import copy
import os


def encryption_block(inputLeft, inputRight, key):
    '''
    input is expected to be 2 ascii characters, or 16 bits. 
    key is expected to be 8 bits.

    Performs a single iteration of a DES block where the input
    is split in half, swapped, then one half is XOR'ed with the key.
    '''
    leftData = inputLeft
    rightData = inputRight

    # Swap the two (copy is used to ensure editing one will not edit the other)
    placeholder = copy.copy(leftData)
    leftData = copy.copy(rightData)
    rightData = placeholder

    # Perform XOR operation on new rightData
    rightData = chr(operator.xor(ord(rightData), ord(key)))

    # Recombine the two sides into 2 characters
    #output = str(leftData + str(rightData))
    return leftData, rightData

def encryption(inputLeft, inputRight, keyList):
    '''
    input is expected to be 2 ascii characters
    keyList is a list of 8 keys which are each 1 character or 8 bits
plaintext
    passes the input through n encryption blocks where n is the number of keys
    '''
    for key in keyList:
        inputLeft, inputRight = encryption_block(inputLeft, inputRight, key)
        #print("After encryption block", inputLeft, inputRight)
    
    return inputLeft, inputRight

def oddEncryption(input, keyList):
    outputLeft, outputRight = encryption(input, input, keyList)

    return outputLeft

def encrypt(keyList, plaintext):
    ciphertext = ""
    if len(plaintext) == 0:
        #print("The infile contains no data!")
        raise RuntimeError

    # If it is, iterate through the unencrypted data and encode it piece by piece 
    #print("Before Encrypting: ", plaintext, type(plaintext))
    
    # Then while inside this loop encrypt the data
    # First need to check that there are an even number of characters
    if len(plaintext)%2 != 0:
        for j in range(0, len(plaintext)-1,2):
            #print("Now Encrypting: ", plaintext[j],plaintext[j+1])
            outputLeft, outputRight = encryption(plaintext[j],plaintext[j+1], keyList)

            #print(type(outputLeft), outputLeft)
            ciphertext = ciphertext + outputLeft + outputRight

        #print("Now Encrypting: ", plaintext[len(plaintext)-1])
        outputLeft = oddEncryption(plaintext[len(plaintext)-1], keyList)

        #print(type(outputLeft), outputLeft)
        ciphertext = ciphertext + outputLeft

    else:
        for j in range(0, len(plaintext),2):
            #print("Now Encrypting: ", plaintext[j],plaintext[j+1])
            outputLeft, outputRight = encryption(plaintext[j],plaintext[j+1], keyList)

            #print(type(outputLeft), outputLeft)
            ciphertext = ciphertext + outputLeft + outputRight

    return(ciphertext)
