map_dict = {'truck/speed': {'10.35.70.29'}, 'truck/proximity': {'10.35.70.29'}, 'truck/pressure': {'10.35.70.29'}, 'truck/light-on': {'10.35.70.29'},
            'truck/wiper-on': {'10.35.70.29'}, 'truck/passengers-count': {'10.35.70.29'}, 'truck/fuel': {'10.35.70.29'}, 'truck/engine-temperature': {'10.35.70.29'}}
# host = peer[0]
host = '10.35.70.29'
# print(map_dict)
# print(map_dict.values())
for key, val in map_dict.items():
    val.remove(host)

print(map_dict)

