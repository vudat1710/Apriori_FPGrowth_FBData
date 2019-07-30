import operator, json

class Apriori:
    def __init__(self, min_sup, min_conf, filepath):
        self.min_sup = min_sup
        self.min_conf = min_conf
        self.filepath = filepath

    def apriori_gen(self, L):
        C = []
        for l1 in L:
            for l2 in L:
                first = l1[0].split(',')
                second = l2[0].split(',')
                k = len(first)
                can_join = True
                for i in range(k - 1):
                    if first[i] != second[i]:
                        can_join = False
                if first[k-1] >= second[k-1]:
                    can_join = False
                if can_join:
                    c = sorted(set(first) | set(second))
                    if not self.has_infrequent_subset(c, L, k):
                        C.append(','.join(list(c)))
        return C

    def find_frequent_1_itemsets(self, filepath, min_sup):
        itemset = {}
        with open(filepath, 'r') as f:
            for line in f.readlines():
                _list = line.split(' ')
                _list = [x.strip() for x in _list]
                a = ''.join(_list[1:])[1:-1]
                a = a.split(',')
                for item in set(a):
                    if item in itemset:
                        itemset[item] += 1
                    else:
                        itemset[item] = 1
        f.close()
        for item in itemset.copy():
            if itemset[item] < min_sup:
                itemset.pop(item, None)

        return sorted(itemset.items(), key=operator.itemgetter(1))

    
    def powerset(self, s, k): #find all subsets of a set
        powerset = []
        for i in range(1, 1 << len(s)):
            _list = [s[j] for j in range(len(s)) if (i & (1 << j))]
            if len(_list) == k:
                powerset.append(_list)
        
        return powerset
    

    def has_infrequent_subset(self, c, L, k):
        subsets = self.powerset(c, k)
        L = [x[0] for x in L]
        for subset in subsets:
            if ','.join(subset) in L:
                return False
        return True

    def generate_association_rules(self, itemset, min_conf, row_count):
        _dict = {}
        if len(itemset) < 2:
            print("No association rules")
        else:
            print ("\nMinimum Confidence Threshold: ", min_conf*100, "%\n")
            print ("Association rules:\n")
            for k in range(1, len(itemset)):
                for pair in itemset[k]:
                    for i in range(1, len(itemset[k][0][0].split(','))):
                        # print(self.powerset(pair[0].split(','), i))
                        for item in self.powerset(pair[0].split(','), i):
                            item_sup = None
                            for j in itemset[i-1]:
                                if j[0] == ",".join(item):
                                    item_sup = int(j[1])
                            if item_sup is not None and pair[1]/float(item_sup) >= min_conf:
                                _dict[",".join(item)] = ",".join(list(set(pair[0].split(',')) - set(item)))
                                print (",".join(item), "=>", ",".join(list(set(pair[0].split(',')) - set(item))), "Support: ", float("{0:.2f}".format(float(item_sup)/row_count))*100, "%", "Confidence: ", float("{0:.2f}".format(pair[1]/float(item_sup)*100)), "%")
        with open('result_likes2.json', 'w') as fi:
            json.dump(_dict, fi)
        fi.close()
    
    def main(self):
        row_count = 0
        with open(self.filepath, 'r') as f:
            for line in f.readlines():
                row_count += 1
        self.min_sup = self.min_sup * row_count
        F1 = self.find_frequent_1_itemsets(self.filepath, self.min_sup)
        itemset = [F1]
        k = 2
        D1 = {}
        with open(self.filepath, 'r') as f:
            for line in f.readlines():
                _list = line.split(' ')
                _list = [x.strip() for x in _list]
                a = ''.join(_list[1:])[1:-1]
                a = a.split(',')
                D1[_list[0]] = a
        dataset = [D1]
        while True:
            if len(itemset[k-2]) == 0:
                break
            C = self.apriori_gen(itemset[k-2])
            D = {}
            F = {}
            for t in dataset[k-2]:
                Ct = {}
                for c in C:
                    temp_c = c.split(',')
                    temp1 = temp_c[:(k-1)]
                    temp2 = temp_c[:(k-2)] + [temp_c[k-1]]
                    if ','.join(temp1) in dataset[k-2][t] and ','.join(temp2) in dataset[k-2][t]:
                        if c in Ct:
                            Ct[c] += 1
                        else:
                            Ct[c] = 1
                for item in Ct:
                    if item in F:
                        F[item] += Ct[item]
                    else:
                        F[item] = Ct[item]
                if (len(Ct) != 0):
                    D[t] = list(Ct.keys())
            for item in F.copy():
                if F[item] < self.min_sup:
                    F.pop(item, None)
            dataset.append(D)
            itemset.append(sorted(F.items(), key=operator.itemgetter(1)))
            k += 1
        itemset.pop()

            

        self.generate_association_rules(itemset, self.min_conf, row_count)
        
if __name__=="__main__":
    min_sup = 0.01
    min_conf = 0.6
    a = Apriori(min_sup, min_conf, 'FacebookGraph/likes2.csv')
    a.main()

