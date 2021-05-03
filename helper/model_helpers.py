import datetime
import random
import time

from HUB import settings


def generate_random_code():
    curr_time = str(int(round(time.time() * 10)))
    return int(str(settings.OBJECT_ID_PREFIX) + str(datetime.datetime.now().year)[2:] + curr_time[2:] + str(random.randrange(0, 100)).zfill(2))


MAX_GENERATE_CODE_LOOP = 10


def unique_id_generator(instance):
    Klass = instance.__class__
    code = generate_random_code()
    check_code_count = 0
    while True:
        qs_exists = Klass.objects.filter(id=code).exists()
        if not qs_exists:
            return code
        check_code_count += 1
        if check_code_count > MAX_GENERATE_CODE_LOOP:
            code += random.randrange(0, check_code_count)
        else:
            code = generate_random_code()
