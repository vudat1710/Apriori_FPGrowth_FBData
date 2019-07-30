import urllib3
import facebook
import requests
import pickle as pkl
import json, csv, sys

class GetData:
    def __init__(self, dirpath, page_id, limit_num_users):
        self.access_token = "EAAAAAYsX7TsBAGANQoiSW8vwMNwN3heBGZBIbAZAW5MPDHncq6JE7Htfhu6R64hsY7f62ex3P5XTIsy53IEWa4gwRUpBJV1T8fBv9gZBHR8RLJqOZCNzuQ2ZCSBTsSl3IY3jAQRgG95VUyXXZAzLLvfepi9UOtm4mKzAGbb0Gr0AZDZD"
        self.graph = facebook.GraphAPI(access_token=self.access_token, version=3.1)
        self.likes = {}
        self.groups = {}
        self.user_ids = []
        self.post_ids = []
        self.dirpath = dirpath
        self.page_id = page_id
        self.limit_num_users = limit_num_users

    def get_user_likes(self, user_id):
        like_user = []
        try:
            try:
                likes_data = self.graph.get_object('/%s?fields=likes.limit(100)' % user_id)['likes']['data']
                for like in likes_data:
                    like_user.append(like['id'])
                    # likes_data = requests.get(likes_data['paging']['next']).json()
                self.likes[user_id] = like_user
                del likes_data
            except KeyError:
                pass
        except facebook.GraphAPIError:
            pass
    
    def get_user_groups(self, user_id):
        group_user = []
        try:
            try:
                groups_data = self.graph.get_object('/%s?fields=groups.limit(100)' % user_id)['groups']['data']           
                for group in groups_data:
                    group_user.append(group['id'])
                # groups_data = requests.get(groups_data['paging']['next']).json()
                self.groups[user_id] = group_user
                del groups_data
            except KeyError:
                pass
        except facebook.GraphAPIError:
            pass
    
    def get_user_id_from_posts(self, post_id):
        comments_data = self.graph.get_object('/%s/comments' % post_id)
        while (True):
            try:
                for comment in comments_data['data']:
                    com_id = comment['from']['id']
                    if com_id not in self.user_ids:
                        self.user_ids.append(com_id)
                comments_data = requests.get(comments_data['paging']['next']).json()
            except KeyError:
                break
    
    def get_post_id_from_page(self, page_id):
        post_data = self.graph.get_object('/%s/feed' % page_id)
        while (True):
            try:
                for post in post_data['data']:
                    post_id = post['id']
                    if post_id not in self.post_ids:
                        self.post_ids.append(post_id)
                if len(self.post_ids) < 100:
                    post_data = requests.get(post_data['paging']['next']).json()
                else: 
                    break
            except KeyError:
                break
    
    def handle(self, filename, data):
        with open('%s/%s' % (self.dirpath, filename), 'w') as f:    
            f_writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for user_id in data.keys():
                f_writer.writerow(data[user_id])
        f.close()
    
    def get_user_data(self, user_id):
        self.get_user_likes(user_id)
        self.get_user_groups(user_id)

    def main(self):
        # self.get_post_id_from_page(self.page_id)
        # for post_id in self.post_ids:
        #     if len(self.user_ids) < self.limit_num_users:
        #         self.get_user_id_from_posts(post_id)
        #         print(len(self.user_ids))
        # with open('%s/user_ids.pkl' % self.dirpath, 'wb') as f:
        #     pkl.dump(self.user_ids, f)
        # with open('%s/user_ids.pkl' % self.dirpath, 'rb') as f:
        #     user_ids = pkl.load(f)
        # f.close()
        # count = 0
        # for i in range(len(user_ids)):
        #     user_id = user_ids[i]
        #     self.get_user_likes(user_id)
        #     self.get_user_groups(user_id)
        #     count += 1
        #     print(count)
        # self.handle('likes.csv', self.likes)
        # self.handle('groups.csv', self.groups)
        self.get_user_data(sys.argv[1])
        # print(self.likes[sys.argv[1]], self.groups[sys.argv[1]])
        return (self.likes[sys.argv[1]], self.groups[sys.argv[1]])
        

if __name__=="__main__":
    dirpath  = 'rec'
    page_id = "223790994475363"
    limit_num_users = 100
    a = GetData(dirpath, page_id, limit_num_users)
    a.main()