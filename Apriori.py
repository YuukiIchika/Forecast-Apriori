#-*-coding:utf-8-*-
import itertools
from collections import defaultdict

class Apriori(object):
    def __init__(self, data, min_sup=2):
        self.data = data
        self.min_sup_val = min_sup

    def apriori(self):
        Lkm1 = self.find_frequent_1_itemsets()
        L = Lkm1

        while Lkm1 != []:
            c_dic = {}
            Ck = self.apriori_gen(Lkm1)
            for datalist in self.data:
                for item in Ck:
                    if set(item) <= set(datalist):      # 如果datalist包含itemn，C[item]++
                        if tuple(item) in c_dic:
                            c_dic[tuple(item)] +=1
                        else:
                            c_dic[tuple(item)] = 1

            Lk = []
            for item in c_dic:
                if c_dic[item] >= self.min_sup_val:
                    Lk.append(list(item))

            Lkm1 = Lk
            L += Lk
        return L

    def find_frequent_1_itemsets(self):
        """
        查找频繁1项集
        """
        freq_cnt = defaultdict(int)         # 带默认值的dict
        for list in self.data:
            for item in list:
                freq_cnt[item] += 1
        global max
        for item in freq_cnt:
            if item > max:
                max = item
        freq_list = []
        for item in freq_cnt:
            if freq_cnt[item] >= self.min_sup_val:
                freq_list.append([item])
        return freq_list

    def apriori_gen(self, Lkm1):
        """
        由L(k-1)生成C(k)
        """
        Ck = []
        k = len(Lkm1[0]) + 1
        for l1 in Lkm1:
            for l2 in Lkm1:
                flag = False
                # 比较除了最后一项，如果不同，则跳出
                for i in range(k - 2):
                    if l1[i] != l2[i]:
                        flag = True
                        break
                if flag: continue
                # 当最后一项 l1 < l2 时，l1与l2最后一项合并
                if l1[k - 2] < l2[k - 2]:
                    c = l1 + [l2[k - 2]]
                else:
                    continue
                # 将没有频繁项集的项排除
                if self.has_infrequent_subset(c, Lkm1):
                    continue
                else:
                    Ck.append(c)
        return Ck

    def has_infrequent_subset(self, Ck, Lkm1):
        """
        返回C(k)的某一项的所有(k-1)项集中是否有非频繁项集
        """
        k = len(Lkm1[0]) + 1
        subsets = list(itertools.combinations(Ck, k - 1))
        for item in subsets:
            item = list(item)
            if item not in Lkm1:
                return True
        return False

if __name__ == '__main__':
    filePath = 'train.TXT'
    dataList = [line.strip().split('\t') for line in open(filePath)]
    data = [data[2:8] for data in dataList[0:]]
    t = Apriori(data, 2)
    L = t.apriori()
    flag = 1
    fiveL = []
    for i in L:
        if len(i) == 5:
            for j in i:
                if j == max:
                    flag = 0;
            if flag:
                i.append(max)
                fiveL.append(i)
    count = 0
    money = 0
    maxAmount = 0
    maxLine = 0
    listCount = 0
    for i in fiveL:
        for line in data:
            for item in line:
                for j in i:
                    if j == item:
                        count += 1
            if count == 0 or 1 or 2:
                money += 5
            if count == 3:
                money += 10
            if count == 4:
                money += 350
            if count == 5:
                money += 6000
            if count == 6:
                money += 4000000
            count = 0
        i.append(money)
        if money > maxAmount:
            maxAmount = money
            maxLine = listCount
        money = 0
        listCount += 1
        print (i)
    print ("the best choice is:")
    print (fiveL[maxLine])
    
