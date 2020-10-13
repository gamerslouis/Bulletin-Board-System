import threading
import redis
import json


class Producer:
    def __init__(self):
        self.username = ''
        self.redis = redis.StrictRedis(host='10.0.8.1', port=6379, decode_responses=True)

    def new_post(self, board, title):
        self.redis.publish('bbs', json.dumps({
            'username': self.username,
            'board': board,
            'title': title
        }))


class Consumer:
    def __init__(self):
        self.subs = []
        self.redis = redis.StrictRedis(host='10.0.8.1', port=6379, decode_responses=True)
        self.r_sub = self.redis.pubsub()
        self.r_sub.subscribe(**{'bbs': self.handlePost})
        self.rlock = threading.RLock()

    def run(self):
        self.thread = self.r_sub.run_in_thread(sleep_time=0.001, daemon=True)

    def stop(self):
        self.thread.stop()

    def handlePost(self, message):
        # try:
        if message['type'] != 'message':
            return
        self.rlock.acquire()

        post = json.loads(message['data'])

        for sub in self.subs:
            if sub['type'] == 'board' and post['board'] == sub['name'] and sub['keyword'] in post['title']:
                print('*[{}] {} – by {}*\n% '.format(post['board'], post['title'], post['username']),end='')
                break
            if sub['type'] == 'author' and post['username'] == sub['name'] and sub['keyword'] in post['title']:
                print('*[{}] {} – by {}*\n% '.format(post['board'], post['title'], post['username']),end='')
                break                
        # except Exception:
        #     print(Exception)

        self.rlock.release()
