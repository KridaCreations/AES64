import math

sbox = [6,11,5,4,2,14,7,10,9,13,15,12,3,1,0,8]
isbox = [14,13,4,12,3,2,0,6,15,8,7,1,11,9,5,8]
rcon=[[1,0,0,0],[2,0,0,0],[4,0,0,0],[8,0,0,0],[3,0,0,0],[6,0,0,0],[12,0,0,0],[11,0,0,0],[5,0,0,0],[10,0,0,0]]
shiftmatrixa = [[0,0,0,0],[1,1,1,1],[2,2,2,2],[3,3,3,3]]
shiftmatrixb = [[0,1,2,3],[3,0,1,2],[2,3,0,1],[1,2,3,0]]
mixmatrix = [[2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]]

def countbits(input):
    count = 0
    inputtemp = input
    while(inputtemp!=0):
        count += 1
        inputtemp = inputtemp>>1
    return count

def modulo(input,mod1):
    bitinput = countbits(input)
    bitmod1 = countbits(mod1)
    while(bitmod1 <bitinput):
        mod1 = mod1<<1
    
    while(input >= 16):
        if(int(math.log(input,2)) == int(math.log(mod1,2))):
            input = input ^ mod1
        mod1 = mod1>>1
    return input

        

def fmul(a,b):
    multiples = []
    while(b != 0):
        if(b %2 == 1):
            multiples.append(a)
        a = a<<1
        b = b>>1
    result = 0
    for i in range(0,len(multiples)):
        result = result ^ multiples[i]

    return modulo(result,19)
def mixcolumn(text):
    result = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for i in range(len(mixmatrix)):
        for j in range(len(text[0])):
            for k in range(len(text)):
                result[i][j] = result[i][j] ^ (fmul(mixmatrix[i][k] , text[k][j]))
    
    return result

def shift(text):
    newtext = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for i in range(0,4):
        for j in range(0,4):
            newtext[shiftmatrixa[i][j]][shiftmatrixb[i][j]] = text[i][j]
    
    return newtext

def substitution(text):
    for i in range(0,4):
        for j in range(0,4):
            text[i][j] = sbox[text[i][j]]

    return text

def keyforward(key,rno):
    # print("inside keyforward " + str(rno))
    #rotword
    col = [0,0,0,0]
    col[0] = key[1][3]
    col[1] = key[2][3]
    col[2] = key[3][3]
    col[3] = key[0][3]
    #subword & xor with round constant
    col[0] = (sbox[col[0]]) ^ rcon[rno][0] 
    col[1] = (sbox[col[1]]) ^ rcon[rno][1]
    col[2] = (sbox[col[2]]) ^ rcon[rno][2]
    col[3] = (sbox[col[3]]) ^ rcon[rno][3]
    #new first columnm
    col[0] = col[0] ^ key[0][0]
    col[1] = col[1] ^ key[1][0]
    col[2] = col[2] ^ key[2][0]
    col[3] = col[3] ^ key[3][0]
    newkey = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    newkey[0][0] = col[0]
    newkey[1][0] = col[1]
    newkey[2][0] = col[2]
    newkey[3][0] = col[3]
    for j in range(1,4):
        for i in range(0,4):
            newkey[i][j] = newkey[i][j-1] ^ key[i][j]
    return newkey
        
    
def encrypt(text,key):
    for i in range(0,4):
        for j in range(0,4):
            text[i][j] = text[i][j] ^ key[i][j]
    
    # print("after round 0")
    # print(text)
    # print(" ")
    key = keyforward(key,0)
    # print("roung key ")
    # print(key)    
    text = round(text,key)
    print("after round 1")
    # print(text)
    # print(" ")
    key = keyforward(key,1)
    # print("roung key ")
    # print(key)
    text = round(text,key)
    print("after round 2")
    # print(text)
    # print(" ")
    key = keyforward(key,2)
    # print("roung key ")
    # print(key)
    text = round(text,key)
    print("after round 3")
    # print(text)
    # print(" ")
    key = keyforward(key,3)
    # print("roung key ")
    # print(key)
    text = round(text,key)
    print("after round 4")
    # print(text)
    # print(" ")
    key = keyforward(key,4)
    # print("roung key ")
    # print(key)
    text = round(text,key)
    print("after round 5")
    # print(text)
    # print(" ")
    key = keyforward(key,5)
    # print("roung key ")
    # print(key)
    text = round(text,key)
    print("after round 6")
    # print(text)
    # print(" ")
    key = keyforward(key,6)
    # print("roung key ")
    # print(key)
    text = round(text,key)
    print("after round 7")
    # print(text)
    # print(" ")
    key = keyforward(key,7)
    # print("roung key ")
    # print(key)
    text = round(text,key)
    print("after round 8")
    # print(text)
    # print(" ")
    key = keyforward(key,8)
    # print("roung key ")
    # print(key)
    text = round(text,key)
    print("after round 9")
    # print(text)
    # print(" ")
    key = keyforward(key,9)
    text = lastround(text,key)
    # print(text)
    return text

def round(text,key):
    # print("inside round")
    text = substitution(text)
    # print("after substitution")
    # print(text)
    text = shift(text)
    # print("after shifting")
    # print(text)
    text = mixcolumn(text)
    # print("after mixcolumn")
    print(text)
    for i in range(0,4):
        for j in range(0,4):
            text[i][j] = text[i][j] ^ key[i][j]
    # print("after adding round key")
    # print(text)
    return text

def lastround(text,key):
    text = substitution(text)
    text = shift(text)
    for i in range(0,4):
        for j in range(0,4):
            text[i][j] = text[i][j] ^ key[i][j]
    return text



text = [[13,12,11,6],[9,8,11,15],[0,15,10,0],[3,14,2,14]]
key = [[8,5,13,6],[11,13,9,3],[6,5,14,1],[13,3,5,10]]
print(encrypt(text,key))