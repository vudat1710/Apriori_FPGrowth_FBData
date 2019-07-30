import operator

class Node:
    def __init__(self):
        self.num_children = 0
        self.children = []
        self.parent = None
        self.count = 0
        self.item = ''

class FP_Tree:
    def __init__(self):
        self.path_result = {}
        self.freq_itemset = {}

    def get_frequent_items(self, filepath, min_sup):
        itemset = {}
        with open(filepath, 'r') as f:
            for line in f.readlines():
                _list = line.split(',')
                _list = [x.strip() for x in _list]
                for item in set(_list):
                    if item in itemset:
                        itemset[item] += 1
                    else:
                        itemset[item] = 1
        f.close()

        for item in itemset.copy():
            if itemset[item] < min_sup:
                itemset.pop(item, None)

        return sorted(itemset.items(), key=operator.itemgetter(1))

    def calc_ordered_itemset(self, filepath, min_sup):
        freq_items = dict(self.get_frequent_items(filepath, min_sup))
        ordered_itemset = []
        with open(filepath, 'r') as f:
            for line in f.readlines():
                orderset = {}
                _list = line.split(',')
                _list = [x.strip() for x in _list]
                for item in _list:
                    if item in freq_items.keys():
                        orderset[item] = freq_items[item]
                # get all item has count >= min_sup in reverse order
                ordered_itemset.append(list(dict(sorted(orderset.items(), key=operator.itemgetter(1), reverse=True)).keys()))
        return ordered_itemset    

    def generate_tree(self, node, order_list, item):
        if len(order_list) == 0:
            return
        for child in node.children:
            if child.item == item:
                child.count += 1
                del order_list[0]
                if len(order_list) == 0:
                    return
                self.generate_tree(child, order_list, order_list[0])
                if len(order_list) == 0:
                    return
                break
        new_node = Node()
        new_node.item = item
        new_node.count += 1
        new_node.parent = node
        node.num_children += 1
        node.children.append(new_node)
        del(order_list[0])
        if len(order_list) == 0:
            return
        self.generate_tree(new_node, order_list, order_list[0])

    def conditional_pattern_base(self, root, item, item_res, path = []):
        if root.item != '':
            path = path + [root.item]
        if root.num_children == 0:
            return
        for child in root.children:
            if str(child.item) == item:
                temp = {}
                key = ','.join(path)
                if key != '':
                    temp[key] = child.count
                    item_res.append(temp)
            else:
                self.conditional_pattern_base(child, item, item_res, path)
        return item_res
                
    
    def conditional_fp_tree(self, min_sup):
        for key in self.path_result.keys():
            key_dict = {}
            conditional_pattern = self.path_result[key]
            if len(conditional_pattern) != 0:
                for element in conditional_pattern:
                    path = list(element.keys())[0]
                    count = element.get(path)
                    _list = path.split(',')
                    for item in _list:
                        if item in key_dict:
                            key_dict[item] += count
                        else:
                            key_dict[item] = count
            for item in key_dict.copy():
                if key_dict[item] < min_sup:
                    key_dict.pop(item, None)
            
            self.freq_itemset[key] = key_dict
        
    def powerset(self, s, k): #find all subsets of a set
        powerset = []
        for i in range(1, 1 << len(s)):
            _list = [s[j] for j in range(len(s)) if (i & (1 << j))]
            if len(_list) == k:
                powerset.append(_list)
        
        return powerset

    def gen_all_powerset_with_sup(self):
        result_dict = {}
        for key in self.freq_itemset.keys():
            result = []
            key_dict = self.freq_itemset[key]
            key_dict_keys = list(set(key_dict))
            for i in range(len(key_dict_keys)):
                result = result + self.powerset(key_dict_keys, i+1)
            for ele in result:
                if len(ele) == 1:
                    ele_with_key = ele + [key]
                    result_dict[','.join(ele_with_key)] = key_dict[ele[0]]
                else:
                    ele_with_key = ele + [key]
                    result_dict[','.join(ele_with_key)] = min(key_dict.items(), key=lambda x: x[1])[1]
        
        return result_dict
    
    def subs(self, l):
        assert type(l) is list
        if len(l) == 1:
            return [l]
        x = self.subs(l[1:])
        return x + [[l[0]] + y for y in x]
    
    def assRule(self, freq, min_conf=0.6):
        assert type(freq) is dict
        result = []
        for item, sup in freq.items():
            for subitem in self.subs(list(item)):
                sb = [x for x in item if x not in subitem]
                if sb == [] or subitem == []:
                    continue
                if len(subitem) == 1 and (subitem[0][0] == "in" or subitem[0][0] == "out"):
                    continue
                conf = sup / freq[tuple(subitem)]
                if conf >= min_conf:
                    result.append({"from": subitem, "to": sb, "sup": sup, "conf": conf})
        return result

    def main(self):
        filepath = 'data.csv'
        row_count = 0
        min_sup = 1.2
        with open(filepath, 'r') as f:
            for _ in f.readlines():
                row_count += 1
        ordered_itemset = self.calc_ordered_itemset(filepath, min_sup)
        root = Node()
        for _list in ordered_itemset:
            self.generate_tree(root, _list, _list[0])
        ordered_items = dict(self.get_frequent_items(filepath, min_sup)).keys()
        for item in ordered_items:
            self.path_result[item] = self.conditional_pattern_base(root, item, [])
        self.conditional_fp_tree(min_sup)
        a = self.gen_all_powerset_with_sup()
        b = dict(self.get_frequent_items(filepath, min_sup))
        z = {**a, **b}
        res_for_rul = {}
        for item in z:
            res_for_rul[tuple(item.split(','))] = z[item]
        print (self.assRule(res_for_rul))

if __name__=="__main__":
    a = FP_Tree()
    a.main()