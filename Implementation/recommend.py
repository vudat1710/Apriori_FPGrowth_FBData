from FacebookGraph.crawl_user_data import GetData
from apriort_mpi import Apriori
import json, pickle

def get_result(likes_file, groups_file):
    with open(likes_file, 'r') as f:
        likes_result = json.load(f)
    f.close()
    with open(groups_file, 'r') as f:
        groups_result = json.load(f)
    f.close()
    return (likes_result, groups_result)

def recommend(dirpath, page_id, limit_num_users):
    get_data = GetData(dirpath, page_id, limit_num_users)
    (likes, groups) = get_data.main()
    (likes_result, groups_result) = get_result('result_likes.json', 'result_groups.json')
    for key in likes_result.keys():
        _list = key.split(',')
        for ele in _list:
            if ele in likes:
                try:
                    print("You should like " + likes_result[ele])
                except KeyError:
                    pass
            else:
                continue

    for key in groups_result.keys():
        _list = key.split(',')
        for ele in _list:
            if ele in groups:
                try:
                    print("You should join " + groups_result[ele])
                except KeyError:
                    pass
            else:
                continue

with open('FacebookGraph/user_ids.pkl', 'rb') as f:
    user_ids = pickle.load(f)

# print(user_ids[45])

recommend(1,2,4)
    
