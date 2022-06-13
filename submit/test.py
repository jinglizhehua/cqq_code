from matplotlib import pyplot as plt
import itertools as it
from collections import defaultdict

tesxing_list = ["tesxing0", "tesxing1"]
MCS_list = ["MCS5", "MCS10"]
esn0_list = ["esn00", "esn01", "esn02"]
file_type_list = ["noise", "postsinr", "presinr"]

def matrixs_to_avg(matrixs):
    sum = 0
    cnt = 0
    for matrix in matrixs:
        for value in matrix:
            sum += value
            cnt += 1
    return sum / cnt

def read_files(file_type):
    global tesxing_list
    global MCS_list
    global esn0_list
    read_data = defaultdict(list)
    
    file_product = it.product(  tesxing_list,
                                MCS_list,
                                esn0_list)

    for tesxing, MCS, esn0 in file_product:
        file_name = "{}-{}-{}-{}.txt".format(tesxing, MCS, esn0, file_type)
        # api
        matrixs = read_file_data(file_name)
        read_data[tesxing+"-"+MCS].append(matrixs_to_avg(matrixs))

    return read_data


def read_file_data(file_name):
    ignore_chars = [" ", "\t", "\n"]
    matrixs = []
    with open(file_name, "r") as read_file:
        for read_str in read_file.readlines():
            read_str_tmp = read_str
            for ignore_char in ignore_chars:
                read_str_tmp = read_str_tmp.replace(ignore_char, "")
            if read_str_tmp == "":
                continue
            elif read_str_tmp[:11] == "FloatMatrix":
                matrixs.append([])
                continue
            else:
                matrixs[-1].append(float(read_str_tmp))
    return matrixs

def main():
    global file_type_list
    global esn0_list

    fig = plt.figure()
    for cnt, filetype in enumerate(file_type_list):
        ax = fig.add_subplot(1, len(file_type_list), cnt+1)
        ax.set_title(filetype)

        read_data = read_files(filetype)
        for line_name in read_data.keys():
            ax.plot(esn0_list, read_data[line_name], label=line_name)
        ax.legend()
    # plt.legend()
    plt.show()

if __name__ == "__main__":
    main()

