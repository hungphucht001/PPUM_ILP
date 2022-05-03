# # Đọc dataset dạng data : sum util : item util
# def load_dataset_util(filename):
#     with open(filename) as f:
#         lines = f.readlines()
#     data = []
#     data_util = []
#     sum_util = []
#     item_list = []
#     for line in lines:
#         part = line.split(':')
#         # Tách phần đầu
#         items = part[0].split()
#         tran = []
#         for item in items:
#             tran.append(item)
#             if item not in item_list:
#                 item_list.append(item)
#         data.append(tran)
#         # Tách phần 2
#         sum_util.append(int(part[1]))

#         # Tách phần 3
#         items = part[2].split()
#         tran_util = []
#         for item in items:
#             tran_util.append(int(item))
#         data_util.append(tran_util)
#     # Kết quả:
#     # data: list of list
#     # sum_util: list
#     # data_util: list of list
#     # item_list: list
#     return data, sum_util, data_util, sorted(item_list)


# data = load_dataset_util('test_hui.txt')
# print(data[0][1])
# print(data[1][1])
# print(data[2][1])


def convert_dict_to_array(dict):
    arr_list_utility = []
    arr_list_utility_label = []
    for row in dict:
        newRow = []
        newLable = []
        for i in row:
            newRow.append(row[i])
            newLable.append(i)
        arr_list_utility.append(newRow)
        arr_list_utility_label.append(newLable)
    return arr_list_utility, arr_list_utility_label[0]

def check_list_in_list(arr1, arr2):
    for i in arr2:
        if i in arr1:
            return True
    return False


def check_list_equal_list(arr1, arr2):
    if len(arr1) != len(arr2):
        return False
    else:
        count = 0
        for i in arr2:
            if i in arr1:
                count += 1
        if count == len(arr1):
            return True
        return False


def check_str_in_str(str_1, str_2):
    for i in str_1:
        if i in str_2:
            return True
    return False