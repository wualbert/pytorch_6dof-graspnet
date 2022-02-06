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
    # Read the category names
    with open('shapenet_id_to_name.txt','r') as cat_names_file:
        cat_name_lns = cat_names_file.readlines()
    cat_names_dict = {}
    for cat_name_ln in cat_name_lns:
        ans = cat_name_ln.split(" ")
        num = ans[0]
        item = (" ".join(ans[1:])).strip()
        cat_names_dict[num]=item
    # The items should only be from these
    desired_cats = {'bottle':'Bottle', 'bowl':'Bowl', 'mug':'mug'}

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
    for desired_cat_dir in desired_cats.values():
        os.mkdir("/".join([store_dir, desired_cat_dir]))


    print(f"Attempting to find {len(file_ids_lns)} shapenet IDs")
    found_paths = []
    for file_id_ln in file_ids_lns:
        file_id = file_id_ln.strip()
        dir_result, file_result = find(file_id+"*", search_dir)
        print(dir_result, file_result)
        type = None
        original_path = None
        if dir_result is not None:
            # Found one in a directory
            dir_results_split = dir_result.split("/")
            for dir in dir_results_split:
                if dir in cat_names_dict:
                    name = cat_names_dict[dir]
                    type = desired_cats[name]
            original_path = str(dir_result)+"/models/model_normalized.obj"
            found_paths.append((original_path,file_id,type))
            # print("found paths", found_paths,"\n")
        elif file_result is not None:
            parsed_file_result = file_result.split(".")
            found_path = parsed_file_result[0]
            original_path = found_path+".obj"
            # Read the file to find the type
            with open(original_path, 'r') as f:
                f_lns = f.readlines()
            for f_ln in f_lns:
                f_words = f_ln.split(" ")
                if "Name" in f_words:
                    for i in range(len(f_words)):
                        f_words[i] = f_words[i].strip()
                    for k in desired_cats.keys():
                        if k in f_words:
                            type = desired_cats[k]
                            break
            if type is None:
                print("File type not found for ", original_path)
                type = "."
            found_paths.append((original_path,file_id,type))
        else:
            print(file_id + " not found!")
            continue
        original_path, file_id, type = found_paths[-1]
        shutil.copyfile(original_path, store_dir+f"/{type}/{file_id}.obj")
    print(f"Found {len(found_paths)} files")