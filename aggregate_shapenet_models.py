import fnmatch
import shutil
import os
import sys
import time

def find(pattern, path):
    # dir_results = []
    # file_results = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                return None, os.path.join(root, name)
                # file_results.append(os.path.join(root, name))
        for name in dirs:
            if fnmatch.fnmatch(name, pattern):
                return os.path.join(root, name), None
                # dir_results.append(os.path.join(root, name))
    return None, None

if __name__ == "__main__":
    assert(len(sys.argv)==2)
    search_dir = str(sys.argv[1])
    print("Searching in directory "+ search_dir)
    # Get the names of the
    with open('shapenet_ids.txt', 'r') as shapenet_ids:
        file_ids_lns = shapenet_ids.readlines()
    # Create directory for found file
    store_dir = f"shapenet_models_{time.time()}"
    # print(f"Storing found files at {store_dir}")
    os.mkdir(store_dir)

    print(f"Attempting to find {len(file_ids_lns)} shapenet IDs")
    found_paths = []
    for file_id_ln in file_ids_lns:
        file_id = file_id_ln.strip()
        dir_result, file_result = find(file_id+"*", search_dir)
        if dir_result is not None:
            # Found one in a directory
            found_paths.append((str(dir_result)+"/models/model_normalized.obj",file_id))
            # print("found paths", found_paths,"\n")
        elif file_result is not None:
            parsed_file_result = file_result.split(".")
            final_path = parsed_file_result[0]
            found_paths.append((final_path+".obj",file_id))
        else: 
            print(file_id + " not found!")
    print(f"Found {len(found_paths)} files")
    for original_path, file_id in found_paths:
        shutil.copyfile(original_path, store_dir+f"/{file_id}.obj")
    