import random
import string

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def generate_random_char_id(number_of_char=4):
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(number_of_char))