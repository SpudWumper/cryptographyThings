import numpy as np
import math
from otherAlgorithms import fastExpMod

#-----------------------------------------------------------------------------------------------------------------
#encrypt using caesar cipher, input is the plaintext message and amount to shift, bool to format as blocks of 5
def caesenc (plain, shift, isFormat):
    alph = "abcdefghijklmnopqrstuvwxyz"
    plain = plain.lower()
    plainNumb = [-1] * len(plain)
    l = len(plain)

    #clean plaintext
    for char in plain:
        if char not in alph:
            plain = plain.replace(char, "")
    
    #convert plaintext letters to number in alphabet
    for pInd,pChar in enumerate(plain):
        for aInd, aChar in enumerate(alph):
            if pChar == aChar:
                plainNumb[pInd] = aInd                
    
    #apply shift
    for ind, i in enumerate(plainNumb):
        if i != -1:
            i = (i + shift) % 26
            plainNumb[ind] = i
    
    #convert numbers to ciphertext, format if necessary
    ciphertext = ""
    for i in plainNumb:
        if i == -1:
            if isFormat == False:
                ciphertext += " "
            elif isFormat == True:
                ciphertext += ""
        else:
            ciphertext += alph[i]
    
    if isFormat == True:
        t = " ".join(ciphertext[i:i+5] for i in range(0, len(ciphertext), 5))
        ciphertext = t

    return ciphertext.upper()
#-----------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------
#encrypt using substitution cipher, given a special key
def subenckey (plain, key):
    alph = "abcdefghijklmnopqrstuvwxyz"
    plain = plain.lower()

    #clean plaintext
    for char in plain:
        if char not in alph:
            plain = plain.replace(char, "")
    
    #given a keyword, create the key
    alph = alph.upper()
    for i in range(len(key), 26):
        prev = key[i-1]
        
        if alph.find(prev) == 25:
            nextL = "A"
        else:
            nextL = alph[alph.find(prev)+1]

        if nextL in key:
            nextL = alph[alph.find(nextL)+1]
        if nextL in key:
            nextL = alph[alph.find(nextL)+1]
        key += nextL
    
    alph = alph.lower()
    
    #grab the index of the plaintext character in the alphabet, and replace it with the letter in the same index in the key
    for pInd,pChar in enumerate(plain):
        for aInd, aChar in enumerate(alph):
            if pChar == aChar:
                index = aInd
                plain = plain.replace(pChar, key[index])

    ciphertext = plain

    t = " ".join(ciphertext[i:i+5] for i in range(0, len(ciphertext), 5))
    ciphertext = t

    return ciphertext
#-----------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------
#hill cipher encryption
def hillEnc(plain, key):
    alph = "abcdefghijklmnopqrstuvwxyz"
    plain = plain.lower()
    key = key.upper()

    #used for key matrix and plaintext vectors
    mShape = int(np.sqrt(len(key)))

    #clean plaintext
    for char in plain:
        if char not in alph:
            plain = plain.replace(char, "")
    
    while(len(plain) % mShape != 0):
        plain += "z"
        
    #generate vectors/matrix from plaintext
    plainNumb = np.full((1, len(plain)), -1)
    plainNumb = plainNumb.squeeze()
    for pInd,pChar in enumerate(plain):
        for aInd, aChar in enumerate(alph):
            if pChar == aChar:
                plainNumb[pInd] = aInd
    plainNumb = plainNumb.reshape(int(len(plain)/mShape), mShape)
    plainNumb = np.transpose(plainNumb)
    
    #generate matrix for key
    keyNumb = np.full((1, len(key)), -1)
    keyNumb = keyNumb.squeeze()
    alph = alph.upper()
    for kInd,kChar in enumerate(key):
        for aInd, aChar in enumerate(alph):
            if kChar == aChar:
                keyNumb[kInd] = aInd
    keyNumb = keyNumb.reshape(mShape, mShape)

    #multiply plaintext and key matrices to get cipher matrix
    ciphMatrix = np.matmul(keyNumb, plainNumb)
    ciphMatrix = ciphMatrix % 26

    #create the cipher text
    ciphertext = ""
    ciphMatrix = np.transpose(ciphMatrix)
    for i in range(0, len(ciphMatrix)):
        for j in range(0, len(ciphMatrix[i])):
            ciphertext += alph[ciphMatrix[i][j]]

    #format ciphertext
    t = " ".join(ciphertext[i:i+5] for i in range(0, len(ciphertext), 5))
    ciphertext = t
    
    return ciphertext
#-----------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------
#autokey cipher
def autokey(plain, key):
    alph = "abcdefghijklmnopqrstuvwxyz"
    plain = plain.lower()
    plainNumb = [-1] * len(plain)

    #clean plaintext
    for char in plain:
        if char not in alph:
            plain = plain.replace(char, "")
    
    #convert plaintext letters to number in alphabet
    for pInd,pChar in enumerate(plain):
        for aInd, aChar in enumerate(alph):
            if pChar == aChar:
                plainNumb[pInd] = aInd
    
    #generate the key - KEYPLAINTEXTPLAINTEXT...
    plain = plain.upper()
    for i in range(len(plain)-len(key)):
        key += plain[i]

    #convert key letters to numbers
    alph = alph.upper()
    kNumb = [-1] * len(key)
    for kInd,kChar in enumerate(key):
        for aInd, aChar in enumerate(alph):
            if kChar == aChar:
                kNumb[kInd] = aInd

    #create the ciphertext
    ciph = [""] * len(plain)
    for i in range(0, len(key)):
        newIndex = ( plainNumb[i] + kNumb[i] ) % 26
        ciph[i] = alph[newIndex]
        
    #format ciphertext
    c = 1
    for i in range(5, len(ciph), 5):
        if i == 5:
            ciph.insert(i, " ")
        else:
            ciph.insert(i+c, " ")
            c += 1
        
    return "".join(ciph)
#-----------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------
#railfence cipher
def railfence(plain, keyLength):
    alph = "abcdefghijklmnopqrstuvwxyz"
    plain = plain.lower()

    #clean plaintext
    for char in plain:
        if char not in alph:
            plain = plain.replace(char, "")
    
    #create containers for each row
    counters = [[]*keyLength for i in range(keyLength)]

    #rowCounter keeps track of what row we are on, and up tells us whether we are moving up or down the rows
    #at each step we put the next letter of the plaintext there and increment
    rowCounter = 0
    up = False
    for i in range(len(plain)):
        if rowCounter == keyLength-1:
            up = True
        if rowCounter == 0:
            up = False
        counters[rowCounter].append(plain[i])

        if not up:
            rowCounter += 1
        if up:
            rowCounter -= 1
    
    #create the ciphertext
    ciphertext = ""
    for i in range(len(counters)):
        for j in range(len(counters[i])):
            ciphertext += counters[i][j]

    #format ciphertext
    t = " ".join(ciphertext[i:i+5] for i in range(0, len(ciphertext), 5))
    ciphertext = t

    return ciphertext.upper()
#-----------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------
#bob encrypts a message, he does not know a, only knows g^a mod p, p, g, and b
def gammalEnc(plain, p, g, gToA, b):
    #create the key: g^a*b mod p
    s = fastExpMod(gToA,b,p)

    enco = ""

    for i in range(len(plain)):
        e = str((int(plain[i]) * s) % p)
        k = math.floor(math.log10(p)) + 1

        if len(e) < k:
            missing = k - len(e)
            for i in range(missing):
                e = "0" + e

        enco += e

    #calculate g^b mod p, to give to Alice to decrypt the ciph
    gToB = fastExpMod(g,b,p)

    return gToB, enco
#-----------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------
def rsaEnc(n, e, m):
    c = []

    for i in range(len(m)):
        c.append(fastExpMod(m[i],e,n))

    return c
#-----------------------------------------------------------------------------------------------------------------