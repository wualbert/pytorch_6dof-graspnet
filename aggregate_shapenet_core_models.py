import fnmatch
import shutil
import os
import sys
import time

def find_dir(pattern, path):
    # dir_results = []
    # file_results = []
    for root, dirs, files in os.walk(path):
        for name in dirs:
            if fnmatch.fnmatch(name, pattern):
                return os.path.join(root, name)
    return None

if __name__ == "__main__":
    item_ids = {'02876657':'Bottle', '02880940':'Bowl', '03797390':'mug'}

    assert(len(sys.argv)==2)
    search_dir = str(sys.argv[1])
    print("Searching in directory "+ search_dir)
    # Get the names of the
    with open('shapenet_ids.txt', 'r') as shapenet_ids:
        file_ids_lns = shapenet_ids.readlines()
    # Create directory for found file
    store_dir = f"shapenet_core_{time.time()}"
    # print(f"Storing found files at {store_dir}")
    os.mkdir(store_dir)
    for item_id in item_ids.values():
        os.mkdir("/".join([store_dir, item_id]))

    for item_id in item_ids.keys():
        item_name = item_ids[item_id]
        print(f"Aggregating {item_id}: {item_name}")
        dir_result = find_dir(item_id+"*", search_dir)
        print(f"Path to {item_name}:", dir_result)
        type = None
        for root, dirs, files in os.walk(dir_result):
            for name in files:
                if fnmatch.fnmatch(name, "*.obj"):
                    file_id = root.split("/")[-2]
                    print("file_id", file_id)
                    file_path = os.path.join(root, name)
                    # print("aggregate store path", store_dir+f"/{item_name}/{file_id}.obj")
                    shutil.copyfile(file_path, store_dir+f"/{item_name}/{file_id}.obj")