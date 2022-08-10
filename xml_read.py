import os
import json
import argparse
from collections import OrderedDict
import xml.etree.ElementTree as elemTree

parser = argparse.ArgumentParser()
parser.add_argument('--path_dir', default="./")
args = parser.parse_args()

path_dir = args.path_dir
fileExt = '.xml'
file_list = [_ for _ in os.listdir(path_dir) if _.endswith(fileExt)]

for file_name in file_list:
    # json
    json_data = OrderedDict()

    # xml
    tree = elemTree.parse(f"{path_dir}{file_name}")

    tree_object = tree.findall('./object')

    json_data['Dataset'] = {"label_path" :path_dir, "src_path" :path_dir}
    size = tree.find('size')
    w, h, d = int(size[0].text), int(size[1].text), int(size[2].text)
    json_data['Images'] = {"width" : w, "height" : h ,"identifier" : file_name[:-4], "depth":d}
    bbox = []
    for i, obj in enumerate(tree_object):
        temp_ord = OrderedDict()
        temp_ord['data'] = obj.find('name').text
        temp_ord['id'] = i+1
        loc = obj.find('bndbox')
        x_1, x_2, y_1, y_2 = int(loc[0].text), int(loc[2].text), int(loc[1].text), int(loc[3].text)
        temp_ord['x'] = [x_1, x_1, x_2, x_2]
        temp_ord['y'] = [y_1, y_1, y_2, y_2]
        bbox.append(temp_ord)

    json_data['bbox'] = bbox

    with open(f'{file_name[:-3]}json', 'w', encoding='utf-8') as make_json:
        json.dump(json_data, make_json,  ensure_ascii=False , indent='\t')
    