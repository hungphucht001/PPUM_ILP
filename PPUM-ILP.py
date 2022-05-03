from pulp import LpMinimize, LpProblem, LpVariable, LpAffineExpression
from HUI import HUI, data, D, utility_Dic, utility
from utils import convert_dict_to_array, check_list_in_list, check_list_equal_list, check_str_in_str

class PPUM_ILP:
    def __init__(self, HUI, data, D, utility_Dic, utility):
        self.M = 80
        self.D_ = []
        self.Is = ['AB','AC','AD']
        self.SHI_TB = []
        self.HUI = HUI(self.M)
        self.NHI_TB = []
        self.D = D
        self.data = data
        print('D:',self.data)
        self.utility = utility
        self.utility_Dic = utility_Dic
        self.SHI_TB, self.NHI_TB = self.filter_NHI_and_SHI_to_HUI()
        self.HUI_TIDs = dict(**self.NHI_TB, ** self.SHI_TB)
    
    def filter_NHI_and_SHI_to_HUI(self):
        '''
            Table 5 => table 6, 7
            HUI -> SHI_TB and NHI_TB

        '''
        SHI_TB = {}
        NHI_TB = {}
        for X in self.HUI:
            newRow = {}
            arr = []
            for row in D:
                for item in row:
                    if X == item:
                        if X not in self.Is:
                            arr.append(row[X])
                        else:
                            arr.append(row[X])
            dict_temp = {}
            dict_temp[X] = arr
            newRow.update(dict_temp) 
            if X not in self.Is:
                NHI_TB.update(newRow)
            else:
                SHI_TB.update(newRow)
        return SHI_TB, NHI_TB

    def index_TIDs(self, si):
        '''
            get index with a value other than 0
        '''
        index_Si = []
        for i in range(len(self.HUI_TIDs[si])):
            if(self.HUI_TIDs[si][i] != 0):
                index_Si.append(i)
        return index_Si

    def check_nhi_in_shi(self, item):
        strItem = ''
        for a in self.Is:
            for i in a:
                for j in item:
                    if j not in strItem and (i == j):
                        strItem += j
        return strItem

    def VP(self,item, arr):
        '''
            Vế phải
        '''
        sum_ = 0
        temp = self.check_nhi_in_shi(item)
        for x in arr:
            if item in self.HUI_TIDs and self.HUI_TIDs[item][x-1] != 0:
                sum_ += self.HUI_TIDs[temp][x-1]
        return (self.HUI[item] - sum_)

    def arr_X(self, TIDs, item):
        arr = []
        for X in self.Is:
            for i in self.index_TIDs(X):
                for j in range(len(TIDs[item])):
                    if i == j and TIDs[item][j] != 0:
                        arr.append(i+1)
        return arr

    def arr_sum(self,item):
        arr_sum = {}
        for X in item:
            dict_aa = {}
            dict_aa[X] = LpAffineExpression()
            arr_sum.update(dict_aa)
        return arr_sum

    def arr_Si(self, arr, temp, deci_variables):
        '''
            {'A': 1*A1 + 1*A5 + 1*A7 + 0, 'B': 1*B1 + 1*B5 + 1*B7 + 0}
            {'A': 1*A2 + 1*A8 + 1*A9 + 0, 'C': 1*C2 + 1*C8 + 1*C9 + 0}
            {'A': 1*A1 + 1*A5 + 1*A8 + 0, 'D': 1*D1 + 1*D5 + 1*D8 + 0}
        '''
        for item_vb in deci_variables:
            for item in arr:
                if(item == item_vb):
                    for i in self.Is:
                        if temp == i:
                            for j in self.index_TIDs(i):
                                arr[item] += deci_variables[item][j+1]
        return arr

    def algorithm(self):
        '''
            Thuật toán
        '''
        NHI_TB_temp = self.NHI_TB.copy()
        for row_nhi in NHI_TB_temp:
            L = []    
            for row_shi in self.SHI_TB:
                arr1 = self.index_TIDs(row_shi)
                arr2 = self.index_TIDs(row_nhi)
                if check_str_in_str(row_nhi,row_shi) and check_list_in_list(arr1,arr2):
                    if check_str_in_str(row_nhi,row_shi) and check_list_equal_list(arr1,arr2):
                        del self.NHI_TB[row_nhi]
                        break
                    else:
                        break
                else:
                    L.append(row_shi)
            if L == self.Is:
                del self.NHI_TB[row_nhi]

        NHI_TB_temp_2 = self.NHI_TB.copy()

        for n_i in NHI_TB_temp_2:
            for n_j in NHI_TB_temp_2:
                arr1 = self.index_TIDs(n_i)
                arr2 = self.index_TIDs(n_j)
                if n_j != n_i and n_j in n_i and check_list_equal_list(arr1,arr2):
                    del self.NHI_TB[n_i]


        #Biến quyết định x, y, z
        deci_variables = {}
        for item in self.Is:
            for X in item:
                dict_aa={}
                dict_aa[X] = {i: LpVariable(name=f"{X}{i}", lowBound=1) for i in range(1, len(data) +1)}
                deci_variables.update(dict_aa)

        # Khởi tạo model
        model = LpProblem(name="resource-allocation", sense= LpMinimize)

        # model SHI_TB
        sum_AB = 0
        for item in self.Is:
            sum = 0
            arr = self.arr_Si(self.arr_sum(item), item, deci_variables)
            for i in arr: 
                sum += utility_Dic[i] * arr[i]
                sum_AB += arr[i]
            model += ((sum) <= self.M -1, item) 

        # model còn lại
        for item in self.NHI_TB:
            X = self.check_nhi_in_shi(item)
            sum_item = 0
            arr = self.arr_X(self.NHI_TB, item)
            arr = list(set(arr))
            for i in X:
                util_ = utility_Dic[i]
                sum_item_2 = 0
                for j in arr:
                    for k in deci_variables:
                        if(k == i):
                            sum_item_2 += deci_variables[k][j]
                sum_item += util_* sum_item_2
            model += ((sum_item) >= self.M - self.VP(item, arr), item)

        # model tổng
        sum_temp = 0
        for i in sum_AB:
            sum_temp += i
       
        model += sum_temp

        print('HUI: ',self.HUI)
        print('SHI_TB: ', self.SHI_TB)
        print('NHI_TB: ', self.NHI_TB)
        
        # Solve the optimization problem
        model.solve()

        dict_variables = {}
        for var in model.variables():
            new_dict={}
            new_dict[var.name] = round(var.value())
            dict_variables.update(new_dict)
            print(f"{var.name}: {round(var.value())}")
        

        # Sửa database
        for row in data:
            newRow = {}
            for i in range(len(row)):
                newRow[utility[i][0]] = (row[i])
            self.D_.append(newRow)

        for row in dict_variables:
            X = row[0]
            Ti = int(row[1:]) - 1
            val = dict_variables[row]
            self.D_[Ti][X] = val

        arr_list_utility = convert_dict_to_array(self.D_)

        print('D`:', arr_list_utility)

PPUM_ILP_ = PPUM_ILP(HUI, data, D, utility_Dic, utility)
PPUM_ILP_.algorithm()
