import hashlib

key = b"flag"
for i in "aqwxszedcvfrtgbnhyujkilopm0123456987_-AZERTYUIOPMLKJHGFDSQWXCVBN":
    for j in "aqwxszedcvfrtgbnhyujkilopm0123456987_-AZERTYUIOPMLKJHGFDSQWXCVBN":
        h = hashlib.sha256(key + i.encode() + j.encode())
        h = h.hexdigest()
        if h.startswith('00'):
            print(key.decode() + i + j)
