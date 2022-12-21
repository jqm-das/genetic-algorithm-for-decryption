
from base64 import decode
import random
import math 
import sys
from typing import Counter 
import time 

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def key():
    thekey = ""
    for x in range(0,26):
        scramble = alphabet[int(random.random() * 26)]
        while scramble in thekey:
            scramble = alphabet[int(random.random() * 26)]
        thekey = thekey + scramble
    return thekey

exkey = key()


def encrypt(s,thekey):
    encrypted = ""
    for i in range (0,len(s)):
        if s[i] not in thekey:
            encrypted = encrypted + s[i]
        else:
            encrypted = encrypted + thekey[alphabet.find(s[i])]
    return encrypted

# ex = encrypt(("hello there!").upper(),exkey)

# print(ex)

def decrypt(s,thekey):
    decrypted = ""
    for i in range (0,len(s)):
        if s[i] not in thekey:
            decrypted = decrypted + s[i]
        else:
            decrypted = decrypted + alphabet[thekey.find(s[i])]
    return decrypted

def count(s):
    k = ""
    for i in alphabet:
        if i in s:
            k = k + i 
    print(k)

def read(file):
    with open(file) as f:
        line_list = [line.strip() for line in f]
    return line_list

ngram = read("ngrams.txt")

def ngramdict(length):
    ndict = dict()
    for i in ngram:
        j = i.split()
        if len(j[0]) == length:
            ndict[j[0].upper()] = int(j[1])
    return ndict

dictlength = 3

ngrams = ngramdict(dictlength)

def blockgram(text,length):
    avg = 0 
    for i in range (0,len(text)-length):
        word = text[i:i+length]
        if word in ngrams:
            avg = avg + math.log(ngrams.get(word),2)
    return avg

# testfile = sys.argv[1]

# testcase = read(testfile)
# test = ""
# for i in testcase:
#     test = test + i.upper() + " "

def decodengram(code):
    ciph = key()
    bestdecoded = encrypt(code,ciph)
    bestscore = blockgram(bestdecoded,3)
    for i in range(0,10000):
        swap1 = int(random.random()*26)
        swap2 = int(random.random()*26)
        while swap2 == swap1:
            swap2 = int(random.random()*26)
        if swap1 < swap2:
            copyciph = ciph[0:swap1] + ciph[swap2] + ciph[swap1+1:swap2] + ciph[swap1] + ciph[swap2+1:]
        else:
            copyciph = ciph[0:swap2] + ciph[swap1] + ciph[swap2+1:swap1] + ciph[swap2] + ciph[swap1+1:]
        decoded = encrypt(code,copyciph)
        score = blockgram(decoded,3)
        if score > bestscore:
            bestscore = score
            bestdecoded = decoded 
            ciph = copyciph
            print(bestscore)
            print(bestdecoded)
            print("----------------------------------------------------") 
    print(bestscore)
    print(bestdecoded)

file = sys.argv[1]

# decodengram(test)

POPULATION_SIZE = 500
NUM_CLONES = 1
TOURNAMENT_SIZE = 20
TOURNAMENT_WIN_PROBABILITY = .75
CROSSOVER_LOCATIONS = 5
MUTATION_RATE = .8 

def create_gen(size):
    pops = []
    for i in range(0,size):
        hold = key()
        while hold in pops:
           hold = key()
        pops.append(hold)
    return pops

def breed(key1,key2):
    childkey = ""
    ls = []
    lets = [] 
    for i in range (0,CROSSOVER_LOCATIONS):
        ind = (int(random.random()*26))
        while ind in ls:
            ind = (int(random.random()*26))
        ls.append(ind)
        lets.append(key1[ind])
    for i in range (0,26):
        if i in ls:
            childkey = childkey + key1[i]
        else:
            j = 0
            while key2[j] in lets or key2[j] in childkey:
                j = j + 1
            childkey = childkey + key2[j]
    return childkey


def mutate(ciph):
    if random.random() < MUTATION_RATE:
        swap1 = int(random.random()*26)
        swap2 = int(random.random()*26)
        while swap2 == swap1:
            swap2 = int(random.random()*26)
        if swap1 < swap2:
            copyciph = ciph[0:swap1] + ciph[swap2] + ciph[swap1+1:swap2] + ciph[swap1] + ciph[swap2+1:]
        else:
            copyciph = ciph[0:swap2] + ciph[swap1] + ciph[swap2+1:swap1] + ciph[swap2] + ciph[swap1+1:]
        ciph = copyciph
    return ciph 

def rankgen(gen):
    ds = dict()
    for ciph in gen:
        decoded = encrypt(file,ciph)
        score = blockgram(decoded,3)
        ds.update({ciph:score}) 
    sortgen = sorted(gen,key = lambda a:ds[a],reverse=True)
    return sortgen

def select(sortgen):
    new_gen = []

    for i in range (0,NUM_CLONES):
        new_gen.append(sortgen[i])
    
    while len(new_gen) < 500:
        team1 = []
        team2 = []
        for i in range(0,TOURNAMENT_SIZE):
            ind = int(POPULATION_SIZE *random.random())
            ind2 = int(POPULATION_SIZE *random.random())
            while ind in team1 or ind == ind2 or ind in team2:
                ind = int(POPULATION_SIZE *random.random())
            team1.append(ind)
            while ind2 in team1 or ind2 in team2:
                ind2 = int(POPULATION_SIZE *random.random())
            team2.append(ind2)

        theteam1 = sorted(team1)
        theteam2 = sorted(team2) 

        ind = 0 
        while random.random() > TOURNAMENT_SIZE: 
            ind = ind + 1

        parent1 = sortgen[theteam1[ind]]
        parent2 = sortgen[theteam2[ind]]
        child = mutate(breed(parent1,parent2))
        if child not in new_gen:
            new_gen.append(child)

    sort_final = rankgen(new_gen)
    decoded = encrypt(file,sort_final[0])
    print(decoded)
    print('--------------------------------------------')
    return sort_final


def genetics():
    first_gen = create_gen(POPULATION_SIZE)
    next_gen = select(rankgen(first_gen))
    for i in range (0,498):
        next_gen = select(next_gen)

        
genetics()


