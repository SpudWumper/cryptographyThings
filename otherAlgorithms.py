#These are misc algs, or algs that encryption/decryption algs use

import pandas as pd
from fractions import Fraction
import math

#-----------------------------------------------------------------------------------------------------------------
#frequency analysis
def freq(k, ciph):
    alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    #frequency analysis for single letters
    if k == 1:
        counter = [0]*26

        for char in ciph:
            if char != " ":
                num = alph.find(char)
                counter[num] += 1
        alphList = [0]*26
        for i,a in enumerate(alph):
            alphList[i] = a
        
        df = pd.DataFrame(counter)
        df.insert(0, "letters", alphList)
        df = df.sort_values(by=0, ascending=False)
        #df = df.transpose()
        return df
    
    #frequency analysis for two letter words/bigrams
    if k == 2:
        counter = [[],[]]
        
        #remove spaces
        for char in ciph:
            if char == " ":
                ciph = ciph.replace(" ", "")
        
        #create list of bigrams and counters for them
        for i,char in enumerate(ciph):
            if i != len(ciph)-1:
                pair = char + ciph[i+1]
                counter[1].append(pair)
                counter[0].append(0)
        
        #remove duplicates
        for i,pp in enumerate(counter[1]):      
            while counter[1].count(pp) > 1:
                counter[1].pop(i)
                counter[0].pop(i)
                
        #count bigrams
        for i,char in enumerate(ciph):
            if i != len(ciph)-1:
                pair = char + ciph[i+1]
                
                for ii,p in enumerate(counter[1]):
                    if pair == p:
                        counter[0][ii] += 1
        
        df = pd.DataFrame({"num":counter[0]})
        df.insert(0, "pairs", counter[1])
        df = df.sort_values(by=["num"], ascending=False)
        df = df.transpose()
        return df

        #for i in range(0, len(counter[0])):
            #print(counter[1][i], ":" , counter[0][i])
    
    #frequency analysis for 3 letter words/trigrams
    if k == 3:
        counter = [[],[]]
        
        #remove spaces
        for char in ciph:
            if char == " ":
                ciph = ciph.replace(" ", "")
        
        #create list of trigrams and counters for them
        for i,char in enumerate(ciph):
            if i <= len(ciph)-3:
                pair = char + ciph[i+1] + ciph[i+2]
                counter[1].append(pair)
                counter[0].append(0)
        
        #remove duplicates
        for i,pp in enumerate(counter[1]):      
            while counter[1].count(pp) > 1:
                counter[1].pop(i)
                counter[0].pop(i)
                
        #count trigrams
        for i,char in enumerate(ciph):
            if i <= len(ciph)-3:
                pair = char + ciph[i+1] + ciph[i+2]
                
                for ii,p in enumerate(counter[1]):
                    if pair == p:
                        counter[0][ii] += 1
        
        df = pd.DataFrame({"num":counter[0]})
        df.insert(0, "trigrams", counter[1])
        df = df.sort_values(by=["num"],ascending=False)
        df = df.transpose()
        return df
#-----------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------
#friedman coincedence index
def friedman(ciph, k):
    #remove spaces
    for char in ciph:
        if char == " ":
            ciph = ciph.replace(" ", "")
        if char == "\n":
            ciph = ciph.replace("\n", "")
            
    #calculate total number of pairs possible
    #totalPairs = (math.factorial(len(ciph))) / (math.factorial((len(ciph) - 2)) * 2)
    totalPairs = 0
          
    #count how many pairs there are
    counter = 0
    
    for i in range(0, len(ciph)):
        letter = ciph[i]
        #print(i)
        
        for j in range(i+k, len(ciph), k):
            #print(j)
            totalPairs += 1
            if letter == ciph[j]:
                counter += 1

    return counter/totalPairs
#-----------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------
def guessK(coIndex):
    k = ((26*(0.0656)) - 1) / ((26*coIndex) - 1)
    return k
#-----------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------
# gives table of letter frequencies for every block of k letters
def fmodk(k, ciph):
    alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    #remove spaces
    for char in ciph:
        if char == " ":
            ciph = ciph.replace(" ", "")
        if char == "\n":
            ciph = ciph.replace("\n", "")
    
    # counters = [0]*k
    # for i in range(0, k):
    #     counters[i] = [0]*26
    counters = [0]*26
    for i in range(0, 26):
        counters[i] = [0]*k
        
    for i in range(0, k):
        for j in range(i, len(ciph), k):
            if ciph[j] != " ":
                num = alph.find(ciph[j])
                counters[num][i] += 1
                        
    alphList = [0]*26
    for i,a in enumerate(alph):
        alphList[i] = a
                    
    pd.set_option('display.max_columns', None)
    df = pd.DataFrame(counters)
    #df.columns = alphList
    df.insert(0, "letters", alphList)
    df = df.transpose()
    return df
#-----------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------
#Using euclidean algorithm and continued fractions, quickly finds inverse of a huge number mod m
def EuclideanQ(mod, n, q = 0):
    r1 = n
    q = mod//n
    r2 = mod - n*q

    if r2 == 1:
        return q
    
    q += Fraction(1,EuclideanQ(r1,r2,q))

    return q
#-----------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------
def fastInvMod(mod, n):
    invFrac = EuclideanQ(mod, n)

    numerator = invFrac.numerator

    if numerator*n % mod == 1:
        return invFrac.numerator
    elif numerator*n % mod == mod-1:
        return -invFrac.numerator
#-----------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------
#split string into length k pieces
def kSplit(s, p):
    numDigits = math.floor(math.log10(p)) + 1

    k = numDigits

    strings = []
    for i in range(0,len(s),k):
        strings.append(s[i:i+k])

    return strings
#-----------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------
def strNum(word):
    alph = "abcdefghijklmnopqrstuvwxyz"

    numstring = ""

    for c in word.lower():
        for aInd, aChar in enumerate(alph):
            if c == aChar:
                if aInd < 10:
                    numstring += "0" + str(aInd+1)
                else:
                    numstring += str(aInd+1)

    return int(numstring)
#-----------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------
def numStr(num):
    alph = "abcdefghijklmnopqrstuvwxyz"

    word = ""

    nums = str(num)

    if len(nums) % 2 != 0:
        nums = "0" + nums

    for i in range(0,len(nums),2):
        indStr = nums[i]+nums[i+1]
        ind = int(indStr)-1

        for aInd, aChar in enumerate(alph):
            if ind == aInd:
                word += aChar
    
    return word
#-----------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------
def bases(num, base):
    nums = []
    
    while num > 0:
        r = num % base
        nums.append(r)
        num = (num - r) // base
    
    nums.reverse()

    newNum = int(''.join([str(n) for n in nums]))

    return newNum
#-----------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------
def fastExpMod(num, power, mod):
    powerBase2 = bases(power,2)

    aList = [num]


    for i in range(math.floor(math.log2(power))):
        num = (num**2) % mod
        aList.append(num)
    
    aList.reverse()
    
    relevantPows = []
    powerBase2 = str(powerBase2)
    for i in range(len(powerBase2)):
        if powerBase2[i] == '1':
            relevantPows.append(aList[i])

    out = 1
    for i in relevantPows:
        out = (out * i) % mod

    return out
#-----------------------------------------------------------------------------------------------------------------

