import random
import string
def create_order_id():
    id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])
    return id