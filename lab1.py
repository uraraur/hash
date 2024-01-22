import hashlib
from statistics import mean, variance
import string
import random as rn
#variant 4 --- sha256

symbols = string.ascii_letters + string.digits + string.punctuation

#--------------------------------------------------------------------------------------------
truncation = 2

message =  "KovalMariiaVitalyivna"
hash_message = hashlib.sha256(message.encode('UTF-8')).hexdigest()
print(hash_message)
hash_message = hash_message[len(hash_message)-truncation:len(hash_message)]

t1_pre = []
t2_pre = []
t1_col = []
t2_col = []

#--------------------------------------------------------------------------------------------
def mod_mes(mes):
    return mes.replace(mes[rn.randint(0, len(mes) - 1)], rn.choice(symbols), 1)
#--------------------------------------------------------------------------------------------

def preimage_first_attack(m):
    n = 0
    hash_temp = "0"
    i = 0

    while hash_message != hash_temp:
        i = i + 1
        n = n + 1
        t = str(n)
        hash_temp = hashlib.sha256(m.encode('UTF-8') + t.encode('UTF-8')).hexdigest()
        hash_temp = hash_temp[len(hash_temp)-truncation:len(hash_temp)]

    t1_pre.append(i)

    print(f"Preimage: {message + str(n)} ---- Hash: {hash_temp}")
    return n

#--------------------------------------------------------------------------------------------


def preimage_second_attack(m):
    temp = m
    hash_temp = "0"
    t = 0

    while hash_message != hash_temp:
        t = t + 1
        temp = mod_mes(temp)
        hash_temp = hashlib.sha256(temp.encode('UTF-8')).hexdigest()
        hash_temp = hash_temp[len(hash_temp)-truncation:len(hash_temp)]

    t2_pre.append(t)
    print(f"Preimage: {temp} ---- Hash: {hash_temp}")
    return temp

#--------------------------------------------------------------------------------------------

def collusion_first_attack(m):
    i = 0
    n = 0
    arr = {}
    message1 = m + str(rn.randint(0, 300))
    hash_message1 = hashlib.sha256(message1.encode('UTF-8')).hexdigest()
    hash_message1 = hash_message1[len(hash_message1)-(truncation*2):len(hash_message1)]

    temp = message1
    hash_temp = hash_message1
    
    while hash_temp not in arr:
        i = i + 1
        arr[hash_temp] = temp
        n = n + 1
        t = str(n)
        temp = message1 + t
        hash_temp = hashlib.sha256(temp.encode('UTF-8')).hexdigest()
        hash_temp = hash_temp[len(hash_temp)-(truncation*2):len(hash_temp)]
        
    t1_col.append(i)    

    print(f"Collusion mes1: {arr[hash_temp]} ---- Hash: {hash_temp}")
    print(f"Collusion mes2: {temp} ---- Hash: {hash_temp}")
    return (arr[hash_temp], temp)

#--------------------------------------------------------------------------------------------

def collusion_second_attack(m):

    t = 0
    arr = {}

    message1 = mod_mes(m + str(rn.randint(0, 300)))
    hash_message1 = hashlib.sha256(message1.encode('UTF-8')).hexdigest()
    hash_message1 = hash_message1[len(hash_message1)-(truncation*2):len(hash_message1)]

    temp = message1
    hash_temp = hash_message1
    
    while hash_temp not in arr:
        t = t + 1
        arr[hash_temp] = temp
        temp = mod_mes(temp)
        while temp in arr.values():
            t = t + 1
            temp = mod_mes(temp)
        hash_temp = hashlib.sha256(temp.encode('UTF-8')).hexdigest()
        hash_temp = hash_temp[len(hash_temp)-(truncation*2):len(hash_temp)]
        
    t2_col.append(t)
    print(f"Collusion mes1: {arr[hash_temp]} ---- Hash: {hash_temp}")
    print(f"Collusion mes2: {temp} ---- Hash: {hash_temp}")
    return (arr[hash_temp], temp)

#--------------------------------------------------------------------------------------------

print(f"Message: {message} ---- Message's hash: {hash_message}")
preimage_first_attack(message)
print(f"Message: {message} ---- Message's hash: {hash_message}")
preimage_second_attack(message)
collusion_first_attack(message)
collusion_second_attack(message)



#for i in range(200):
    #test = message + str(rn.randint(0, 1000000))

    #preimage_first_attack(test)
   # preimage_second_attack(test)
    #collusion_first_attack(test)
   # collusion_second_attack(test)

#for i in range(200):
    #test = mod_mes(message)

    #preimage_first_attack(test)
    #preimage_second_attack(test)
    #collusion_first_attack(test)
    #collusion_second_attack(test)

#print(t1_pre)
#print(f"mean: {mean(t1_pre)}, var: {variance(t1_pre)}")
#print(t2_pre)
#print(f"mean: {mean(t2_pre)}, var: {variance(t2_pre)}")
#print(t1_col)
#print(f"mean: {mean(t1_col)}, var: {variance(t1_col)}")
#print(t2_col)
#print(f"mean: {mean(t2_col)}, var: {variance(t2_col)}")



