from tqdm import tqdm

import os
import re
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('-root', type=str, help='root path of a dataset dir')
parser.add_argument('-target', type=str, help='target path of a dataset dir')
parser.add_argument('-key', type=str, help='the key help to identify file under target dir')

parser.add_argument('--model', type=str, help='standardized model [ rn / cp]')
parser.add_argument('--seq', type=bool, default=False, help='a sequence dataset or not? [ True / False]')
# parser.add_argument('--gap', type=str, default='', help='gap between root and sub dir')
parser.add_argument('--prefix', type=str, default='', help='the prefix of standardized name eg.[ rs_0000.jpg ]')
parser.add_argument('--infix', type=str, default='', help='the infix of standardized name eg.[ 0000_rs.jpg ]')
arg = parser.parse_args()

def extract_number(line):
    p = '\d+'
    num_list = re.findall(p, line)
    return list(map(int, num_list))[0]

def standardize_Unit(root, target):
    print('standardized {}'.format(root))
    # print('make target dir: {}'.format(target))
    os.makedirs(target, exist_ok=True)

    # print('get the file list in root dir and sort them')
    file_list = list(filter(lambda x:(arg.key in x), os.listdir(root)))
    file_list.sort(key=lambda x:extract_number(x))

    # print('standardizing ....')
    suffix = file_list[0].split('.')[-1]
    for (i, fname) in enumerate(tqdm(file_list)):
        fname_new = '{}{:05d}{}.{}'.format(arg.prefix, i, arg.infix, suffix)
        if arg.model in ['rn', 'RN']:
            os.rename(os.path.join(root, fname), os.path.join(root, fname_new))
        elif arg.model in ['cp', 'CP']:
            shutil.copy(os.path.join(root, fname), os.path.join(target, fname_new))
    print('standardized sucess!')

def main():
    assert os.path.isdir(arg.root) , 'root dir do not exists!'
    if arg.seq:
        dir_list = list(filter(lambda pth:os.path.isdir(os.path.join(arg.root,pth)), os.listdir(arg.root)))
        for dir in dir_list:
            standardize_Unit(os.path.join(arg.root,dir), os.path.join(arg.target,dir))
    else:
        standardize_Unit(arg.root, arg.target)

if __name__ == '__main__':
    main()