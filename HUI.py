from ast import Return
import numpy as np
from readFile import read_D, read_U
from utils import convert_dict_to_array

data = read_D('data.csv')
utility_Dic, utility = read_U('utility.csv')

def D_Single(data, utility):
    D_single = []
    for row in data:
        newRow = {}
        for i in range(len(row)):
            util = int(utility[i][1])
            newRow[utility[i][0]] = (row[i] * util)
        D_single.append(newRow)
    return D_single

def U_x(list):
    # Định nghĩ 5
    arr_list_utility, arr_list_utility_label = convert_dict_to_array(
        list)

    list_utility_sum = np.array(arr_list_utility)
    col_totals = list_utility_sum.sum(axis=0)
    sum_dict = {}
    for i in range(len(arr_list_utility_label)):
        sum_dict[arr_list_utility_label[i]] = col_totals[i]
    return sum_dict

def myHUI(D_1, D_2, x, D_New, Ux1):
    if x == (len(D_1[0]) - 1):
        return D_New, Ux1
    else:
        i = 0
        D_temp = []
        for row in D_2:
            newRow = {}
            new_value = list(row.items())
            new_val2 = list(D_1[i].items())
            for item in (new_value):
                for item2 in new_val2:
                    if item2[0] in item[0]:
                        continue
                    
                    lable = item[0] + item2[0]
                    value = 0
                    if(item[1] != 0 and item2[1] != 0):
                        value = item[1] + item2[1]
                    newRow[lable] = value

            newRow2 = {}
            lit = list(newRow.items())

            lt_temp = []
            for item in lit:
                y = list(item)
                y[0] = ''.join(sorted(y[0]))
                item = tuple(y)
                lt_temp.append(item)

            for j in range(0, len(lt_temp) - 2):
                for k in range(j + 1, len(lt_temp) -1):
                    if ''.join(sorted(lt_temp[j][0])) in ''.join(sorted(lt_temp[k][0])):
                        del lt_temp[k]
                        break

            for j in range(0, len(lt_temp)):
                newRow2[lt_temp[j][0]] = lt_temp[j][1]

           
            D_New.append(newRow2)
            D_temp.append(newRow2)
            i = i+1
        ux_ = U_x(D_temp)
        Ux1.update(ux_)
        return myHUI(D_1, D_temp, x + 1, D_New, Ux1)

def HUI(M):
    HUI = {}
    for i in Ux:
        if(Ux[i] >= M):
            HUI[i] = Ux[i]
    return HUI

def D_and_Ux():
    D_Temp = []
    D = []
    Ux = {}
    d_Single = D_Single(data, utility)
    D.extend(d_Single)
    Ux.update(U_x(d_Single))
    myHUI(d_Single, d_Single, 1, D_Temp, Ux)
    D.extend(D_Temp)
    return D, Ux

D, Ux = D_and_Ux()
