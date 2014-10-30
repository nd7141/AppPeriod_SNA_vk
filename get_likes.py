import urllib
import json
import time
import pprint

# count = 10
d = dict()

def like_friend(uid, count=10):
    num_likes = 0
    norm = count
    for i in range(1,count):
        response = urllib.urlopen("https://api.vk.com/method/wall.get?owner_id=%d&count=%d" % (uid,count)) # import frends from all_ids.json
        data = json.load(response)
        try:
            like = data["response"][i]["likes"]["count"]
        except IndexError:
            norm = i
            break
        except KeyError:
            break
        except:
            pass
        num_likes+=like
    norm_likes = float(num_likes)/norm
    d[uid] = norm_likes
    with open("id2likes%s.json" %file_ix, "w+") as f:
        json.dump(d, f)
    print norm_likes

# start = time.time()
# like_friend(5277394, 1)
# print time.time() - start
file_ix = 23
with open("all_ids%s.json" %file_ix) as fp:
    all_ids = json.load(fp)

# separate all ids to 4 equal chunks
#http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
# N = 24
# def chunks(l, k):
#     return [l[i:i+k] for i in xrange(0, len(l), k)]

# C = chunks(all_ids, len(all_ids)//N + 1)
# for i in range(N):
#     with open("all_ids%s.json" %i, "w+") as fp:
#         json.dump(C[i], fp)



start = time.time()
for i, uid in enumerate(all_ids):
    print i,
    like_friend(uid, 20)
print time.time() - start

with open("id2likes%s.json" %file_ix, "w+") as f:
    json.dump(d, f)