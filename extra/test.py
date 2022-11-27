# import time 

languages = {'Python', 'Java', 'English'}

# time.sleep(5)
# # remove English from the set
# languages.remove('English')
# self.peers.remove(peer)

# print(languages)

import threading
import time

def removeDueToInactivity(peer):
    languages.remove(peer)
    print(languages)

t = threading.Timer(5, removeDueToInactivity, ['Python'])
t.start()
print(languages)