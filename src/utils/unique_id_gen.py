import random
import time

def generated_unique_id():
    random_number = int(time.time())//10000 + random.randint(100, 999)
    return random_number