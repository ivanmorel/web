import itertools
import time
server = ['SERVER1', 'SERVER2', 'SERVER3', 'SERVER4']
itera = itertools.cycle(server)


def get_server():
    return itera.next()

while True:
    time.sleep(.5)
    print(get_server())
