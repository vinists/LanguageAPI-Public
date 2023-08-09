import time


def get_epoch_filename(ext):
    return f"{str(time.time()).split('.')[0]}.{ext}"
