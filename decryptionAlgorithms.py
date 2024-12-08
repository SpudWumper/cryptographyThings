import numpy as np
import sympy as sym
from collections import deque
from otherAlgorithms import fastExpMod, fastInvMod


#-----------------------------------------------------------------------------------------------------------------
#substitution cipher w/ special key decryption
def subspdec(ciph, subspeckey):
    alph = "abcdefghijklmnopqrstuvwxyz"
    
    #given a keyword, create the key
    alph = alph.upper()
    for i in range(len(subspeckey), 26):
        prev = subspeckey[i-1]
        
        if alph.find(prev) == 25:
            nextL = "A"
        else:
            nextL = alph[alph.find(prev)+1]
            
        if nextL in subspeckey:
            nextL = alph[alph.find(nextL)+1]
        subspeckey += nextL
        
    alph = alph.lower()
    
    #grab index of letter in ciphertext
    for cInd, cChar in enumerate(ciph):
        for sInd, sChar in enumerate(subspeckey):
            if cChar == sChar:
                ciph = ciph.replace(cChar, alph[sInd])
    
    return ciph.lower()
#-----------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------
#vigenere decrypt
def vigenereDecr(mainKey, ciph):
    alph = "abcdefghijklmnopqrstuvwxyz"
    ciph = ciph.lower()
    ciphNumb = [-1] * len(ciph)
    
    #remove spaces
    for char in ciph:
        if char == " ":
            ciph = ciph.replace(" ", "")
        if char == "\n":
            ciph = ciph.replace("\n", "")

    #convert ciphtext letters to number in alphabet
    for cInd,cChar in enumerate(ciph):
        for aInd, aChar in enumerate(alph):
            if cChar == aChar:
                ciphNumb[cInd] = aInd
    
    #given a keyword, create the keys
    alph = alph.upper()
    kNumb = [-1] * len(mainKey)
    for kInd,kChar in enumerate(mainKey):
        for aInd, aChar in enumerate(alph):
            if kChar == aChar:
                kNumb[kInd] = aInd
    print(kNumb)
    
    #create plaintext
    plain = [""] * len(ciph)
    for i in range(0, len(mainKey)):
        for j in range(i, len(plain), len(mainKey)):
            #print(ciphNumb[j], kNumb[i])
            newIndex = ( ciphNumb[j] - kNumb[i] )
            if newIndex < 0:
                newIndex = (ciphNumb[j] + 26) - kNumb[i]
            plain[j] = alph[newIndex]
            
    c = 1
    for i in range(5, len(plain), 5):
        if i == 5:
            plain.insert(i, " ")
        else:
            plain.insert(i+c, " ")
            c += 1        
    
    plain = "".join(plain)
    plain = plain.lower()
            
    return "".join(plain)
#-----------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------
#hill decryption
def hillDec(ciph, key):
    alph = "abcdefghijklmnopqrstuvwxyz"
    alph = alph.upper()
    mShape = int(np.sqrt(len(key)))

    #remove spaces
    for char in ciph:
        if char == " ":
            ciph = ciph.replace(" ", "")
        if char == "\n":
            ciph = ciph.replace("\n", "")

    #generate vectors/matrix from ciphertext
    ciphNumb = np.full((1, len(ciph)), -1)
    ciphNumb = ciphNumb.squeeze()
    for pInd,pChar in enumerate(ciph):
        for aInd, aChar in enumerate(alph):
            if pChar == aChar:
                ciphNumb[pInd] = aInd
    ciphNumb = ciphNumb.reshape(int(len(ciph)/mShape), mShape)
    ciphNumb = np.transpose(ciphNumb)

    #generate matrix for key
    keyNumb = np.full((1, len(key)), -1)
    keyNumb = keyNumb.squeeze()
    alph = alph.upper()
    for kInd,kChar in enumerate(key):
        for aInd, aChar in enumerate(alph):
            if kChar == aChar:
                keyNumb[kInd] = aInd
    keyNumb = keyNumb.reshape(mShape, mShape)

    #get the inverse of key matrix
        #can use sympy.Matrix.inv_mod, but keyNumb will need to be a sympy Matrix
    keyNumb = sym.Matrix(keyNumb)
    keyInverse = keyNumb.inv_mod(26)
    #keyInverse = np.linalg.inv(keyNumb)

    #get plaintext numbers by doing key inverse matrix*ciph matrix % 26
    plainNumb = np.matmul(keyInverse, ciphNumb) % 26

    #create plaintext
    plaintext = ""
    plainNumb = np.transpose(plainNumb)
    alph = alph.lower()
    for i in range(0, len(plainNumb)):
        for j in range(0, len(plainNumb[i])):
            plaintext += alph[plainNumb[i][j]]

    #format plaintext
    t = " ".join(plaintext[i:i+5] for i in range(0, len(plaintext), 5))
    plaintext = t

    return plaintext
#-----------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------
#railfence decryption
def railfenceDec(ciph, keyLength):
    #remove spaces
    for char in ciph:
        if char == " ":
            ciph = ciph.replace(" ", "")
        if char == "\n":
            ciph = ciph.replace("\n", "")

    #create rows
    counters = [deque([])*keyLength for i in range(keyLength)]

    #rowcounter tells what row we are on, up tells us if going up or down the rows
    #fill the correct amount of spaces with empty strings 
    rowCounter = 0
    up = False
    for i in range(len(ciph)):
        if rowCounter == keyLength-1:
            up = True
        if rowCounter == 0:
            up = False
        counters[rowCounter].append("")

        if not up:
            rowCounter += 1
        if up:
            rowCounter -= 1

    #fill the rows going left to right, top to bottom with letters from cipher text
    ciphNumb = 0
    for i in range(len(counters)):
        for j in range(len(counters[i])):
            counters[i][j] = ciph[ciphNumb]
            ciphNumb +=1

    #create the plaintext by reading the letters the same way we filled the rows above
    plaintext = ""
    rowCounter = 0
    up = False
    for i in range(len(ciph)):
        if rowCounter == keyLength-1:
            up = True
        if rowCounter == 0:
            up = False
        

        plaintext += counters[rowCounter].popleft()

        if not up:
            rowCounter += 1
        if up:
            rowCounter -= 1

    #format plaintext
    t = " ".join(plaintext[i:i+5] for i in range(0, len(plaintext), 5))
    plaintext = t

    return plaintext.lower()
#-----------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------
def gammalDec(ciph, p, g, a, gToB):
    #create the key: g^b*a mod p
    s = fastExpMod(gToB,a,p)

    #calculate inverse of the key to decrypt
    invS = fastInvMod(p,s)

    deco = ""

    for i in range(len(ciph)):
        d = str((int(ciph[i]) * invS) % p)

        if len(d) % 2 != 0:
            d = "0" + d

        deco += d

    return deco
#-----------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------
def rsaDec(p, q, e, c):
    n = p*q
    phiN = (p - 1) * (q - 1)

    d = fastInvMod(phiN, e)

    m = []

    for i in range(len(c)):
        m.append(fastExpMod(c[i],d,n))

    return m
#-----------------------------------------------------------------------------------------------------------------