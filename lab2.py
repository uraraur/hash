import hashlib as hl
import random
#variant 4 --- sha256

N = 10000
K = [2**5, 2**6, 2**7]
L = [2**5, 2**6, 2**7]

n = 32 
truncation = n // 8
pad = 128 - n 

#--------------------------------------------------------------------------------------------

def generate_bytes(len):
    return random.randbytes(len).hex()

#r = generate_bytes(pad // 8)
def R(x, r):
    return (r + x)

def gen_hash(t):
    res = hl.sha256(bytes.fromhex(t)).hexdigest()
    return res[len(res) - truncation : len(res)]

#--------------------------------------------------------------------------------------------

def generate_table(K, L):
    r = generate_bytes(pad // 8)
    X = {}

    for i in range(K):
        x_i0 = generate_bytes(n // 8)
        x_ij = x_i0
        for j in range(L): 
            x_ij = gen_hash(R(x_ij, r))
        X[x_ij] = x_i0

    return X, r

def preimage_search(K, L, table, hash_value):
    y = hash_value
    X = table[0]
    r = table[1]
    
    for j in range(L):
        if y in X:
            x = X[y]
            for m in range(L - j - 1):
                x = gen_hash(R(x, r))
            return R(x, r)
        y = gen_hash(R(y, r))

    return 0

def multi_preimage_search(K, L, Xarr, hash_value):
    y = [hash_value] * K
    
    for j in range(L):
        i = 0
        for (X, r) in Xarr:
            if y[i] in X:
                x = X[y[i]]
                for m in range(L - j - 1):
                    x = gen_hash(R(x, r))
                return R(x, r)
            y[i] = gen_hash(R(y[i], r))
            i = i + 1

    return 0


#--------------------------------------------------------------------------------------------
results = []
success = 0
X, r = generate_table(K[2], L[2])
for i in range(N):
    x = generate_bytes(256 // 8)
    h_x = gen_hash(x)
    preim = preimage_search(K[2], L[2], (X, r), h_x)
    if preim != 0:
        results.append((x, preim))
        #print(f"i: {i}, x: {x}, h_x: {h_x}, preim: {preim}")

for (x, p) in results:
    if gen_hash(x) == gen_hash(p):
        #print(f"x: {x}, h_x: {gen_hash(x)}, preim: {p}")
        success = success + 1

print(len(results))
print(success)



results = []
success = 0
tables = []
m = 2
l = 2
for i in range(K[m]):
    tables.append(generate_table(K[m], L[l]))
for i in range(N):
    x = generate_bytes(256 // 8)
    h_x = gen_hash(x)
    preim = multi_preimage_search(K[m], L[l], tables, h_x)
    if preim != 0:
        results.append((x, preim))
        #print(f"i: {i}, x: {x}, h_x: {h_x}, preim: {preim}")

for (x, p) in results:
    if gen_hash(x) == gen_hash(p):
        #print(f"x: {x}, h_x: {gen_hash(x)}, preim: {p}")
        success = success + 1

print(len(results))
print(success)