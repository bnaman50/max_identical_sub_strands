import glob
from  difflib import SequenceMatcher
from srblib import  abs_path
import os
import operator
from itertools import combinations
from collections import  defaultdict
import sys

def find_identical_substr(binX, binY):
    """
    Find identical substring among two binary files along with offsets
    :param binX: binary data of file X
    :param binY: binary data of file Y
    :return: offset_a, offset_b, len(Max_Identical_Subsequence)
    """
    s = SequenceMatcher(None, binX, binY)
    out = s.find_longest_match(0, len(binX), 0, len(binY))
    return out.a, out.b, out.size ## (a=x_idx, b=y_idx, size=N)

def read_binary_file(file_name, file_read_flag, file_data_list):
    """
    Read the data from binary file
    I am storing the data of all the files and making sure that I dont' have to read it again anad again
    (Balance of space and time complexity is imp.
    I am assuming file sizes are small and we can store their data in the memory)
    :param file_name: Name of file
    :param file_read_flag: Flag (list) to check whether file has already been read
    :param file_data_list: list to store file data
    :return: binary file data
    """
    fIdx = get_fIdx(file_name)
    if file_read_flag[fIdx] == 0:
        with open(file_name, mode='rb') as file:  # b is important -> binary
            data = file.read()
        file_data_list[fIdx] = data
        file_read_flag[fIdx] = 1

    return file_data_list[fIdx], fIdx

def get_fIdx(file_name):
    """
    Get file index from file name. Name: Sample.x. Idx = x - 1
    :param file_name: file name
    :return: file idx
    """
    return int(file_name.split('/')[-1].split('.')[-1]) - 1

def file_idx_to_file_name(f_idx, bin_files):
    """
    Converts file idx to fine name. File idx = x-1. File Name = Sample.x
    :param f_idx: Index of file
    :param bin_files: list of names (paths) of binary files
    :return: file name
    """
    f_name = bin_files[f_idx].split('/')[-1]
    return f_name

def get_offset(my_tuple, file_idx):
    """
    MIS(x, y) = maximum identical subsequence between files represented by idx x and y
    :param my_tuple: Tuple containing all information. ((x, y), (x.offset, y.offset, MIS(x, y)))
    :param file_idx: file idx for which you want offset
    :return: file_idx.offset
    """
    pair_idxs = my_tuple[0]
    pair_offsets = my_tuple[1][:-1]
    file_offset = pair_offsets[pair_idxs.index(file_idx)]
    return file_offset

def main(inp_dir):
    ## Read the files. Sort them according to their number
    inp_dir = abs_path(inp_dir)
    bin_files = [file for file in glob.glob(os.path.join(inp_dir, f"sample.*"))]
    bin_files = sorted(bin_files, key=lambda x: get_fIdx(x))

    ## List of flags and list where file data are stored
    file_read_flag = [0]*len(bin_files)
    file_data = [0]*len(bin_files)

    ## Iterate over all pairs of files
    file_pairs = list(combinations(bin_files, 2))
    res = defaultdict(list) # dict. key = size of MIS(x, y). Values- all the pairs where this size happens
    for loop_idx, (fX, fY) in enumerate(file_pairs):
        fX_data, fX_idx = read_binary_file(fX, file_read_flag, file_data)
        fY_data, fY_idx = read_binary_file(fY, file_read_flag, file_data)
        out = find_identical_substr(fX_data, fY_data)
        res[out[2]].append(((fX_idx, fY_idx), out))

    # find the maximum length and list of all pairs of file idxas for which this is true
    max_len, pairs = max(res.items(), key=operator.itemgetter(0))

    # ## This is quite helpful for debugging
    # if sys.gettrace() is not None:
    #     pairs = res[8192]
    #     max_len = 8192

    ## Differentiate files which has different identitcal subsequences.
    ## For ex - (F1, F2, F3 -- mis('abc') -- 3), (F5, F6, F7, F8 -- mis('xyz') -- 3) ## mis represents - MIS(F1, F2)
    unq_datas = defaultdict(list)
    for pr in pairs:
        X_idx = pr[0][0]
        X_offset = pr[1][0]
        X_MIS_len = pr[1][2]
        dt = file_data[X_idx][X_offset:X_offset + X_MIS_len]
        unq_datas[dt].append(pr)

    ## Print the output in readable (hopefully self-explanatory) format
    print(f'The length of maximum strand is {max_len}. '
          f'It occurs in following sets of files\n')

    for l_idx, vals in enumerate(unq_datas.values()):
        print(f'Set: {l_idx+1}/{len(unq_datas)}')
        print(f'Its files and corresponding offsets are as follows:')

        ## File idxs
        file_idxs = [i[0] for i in vals]
        file_idxs = list(set(list(sum(file_idxs, ()))))

        ## File idxs to file names
        file_names = [file_idx_to_file_name(i, bin_files) for i in file_idxs]

        for f_name in file_names:
            val = list(filter(lambda x:get_fIdx(f_name) in x[0], vals))[0] #val where that index exists
            offset = get_offset(val, get_fIdx(f_name))
            print(f'File name: {f_name}, Offset: {offset}')

        print('\n')

if __name__ == '__main__':
    dir_name = 'Eluvio_Challenge_Core_Engineering'
    main(dir_name)
