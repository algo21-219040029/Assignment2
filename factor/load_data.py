
import os
import pickle
from pathlib import Path

__all__ = ['local_data']

file_path = str(Path(__file__).parent.parent.joinpath("data"))
file_list = os.listdir(file_path)

local_data = {}

for file in file_list:
    field = file.replace(".pkl","")
    with open(file_path+'/'+file,'rb') as f:
        data = pickle.load(f)
    local_data[field] = data