import sha3, copy, binascii, miller_rabin, math
from operator import mod, xor

DATASET_BYTES_INIT = 1073741824 # 2^30
DATASET_BYTES_GROWTH = 8388608 # 2 ^ 23
CACHE_BYTES_INIT = 16777216 # 2**24 number of bytes in dataset at genesis
CACHE_BYTES_GROWTH = 131072 # 2**17 cache growth per epoch
CACHE_MULTIPLIER = 1024 # Size of the DAG relative to the cache
EPOCH_LENGTH = 30000 # blocks per epoch
MIX_BYTES = 128 # width of mix
HASH_BYTES = 64 # hash length in bytes
DATASET_PARENTS = 256 # number of parents of each dataset element
CACHE_ROUNDS = 3 # number of rounds in cache production
ACCESSES = 64
WORD_BYTES = 4

def isprime(x):
    for i in range(2, int(x**0.5)):
         if x % i == 0:
             return False
    return True

def get_cache_size(epoc):
    
    sz = CACHE_BYTES_INIT + CACHE_BYTES_GROWTH * epoc
    sz -= MIX_BYTES

    while not isprime(sz / HASH_BYTES):
        sz -= 2 * HASH_BYTES
    return sz

def get_full_size(epoch):
    sz = DATASET_BYTES_INIT + (DATASET_BYTES_GROWTH * epoch)
    sz -= 2 * MIX_BYTES
    while not isprime(sz/MIX_BYTES):
        sz -= 2* MIX_BYTES
    return sz

def get_epoch(block_number):
    return math.floor(block_number / EPOCH_LENGTH)

def get_seed(seed, begin, end):
    seed_hash = seed
    for i in range(begin, end):
        seed_hash = sha3.keccak_256(seed_hash)
    return seed_hash

def fnv(x, y):
    return mod(xor(((x * 0x01000193) | 0), y), 2**32)

def fnv_buffer(a, b):
    bytes_a = bytes(a)
    bytes_b = bytes(b)
    r = b''
    for i in range(0, len(a), 4):
        r += fnv(bytes_a[i:i+4], bytes_b[i:i+4])
    
get_cache_size(1)