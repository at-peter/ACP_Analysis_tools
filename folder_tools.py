from copy import copy
import os
import shutil


def copy_folder(source, destination):
    
    # Read source directory tree
    # read destination directory tree
    max_source_value, source_dir_list = extract_directory_tree(source)
    max_destination_value, dest_dir_list = extract_directory_tree(destination)
    
    print('destination', max_destination_value, dest_dir_list)
    print('source', max_source_value,source_dir_list)
    
    for i, e in enumerate(source_dir_list):
        source_item_path = source + '/' +str(e)
        destination_number = max_destination_value + i + 1 
        destination_path = destination + '/' +str(destination_number)
        # print(source_item_path, destination_number, destination_path)
        # os.mkdir(destination_path)
        move_files(source_item_path, destination_path)


    # for each value in the the list: 
    # copy all the directories into 

def move_files(source_path, destination_path):
    try: 
        print('copying:', source_path )
        shutil.copytree(
            source_path,
            destination_path,
            symlinks=False,
            ignore=None,
            copy_function=shutil.copy2,
            ignore_dangling_symlinks=False,
            dirs_exist_ok=False )
    except:
        print("transfer failed for", source_path)
    return None


def extract_directory_tree(path):
    # need to move os to the location in path 
    cwd = os.getcwd()
   
    os.chdir(path)
    x = os.listdir()

    # get rid of _sources directory: 
    y = max(x)
    x.remove(y)

    # convert the str into ints
    z = list(map(int,x))
    # get the final value that is in the list:
    
    max_val = max(z)

    # sort the list 
    z.sort()

    # at the end, change back to the original working directory
    os.chdir(cwd)
    return max_val, z 

def _main():
    # path1 = 'C:/Users/Wintermute/Desktop/hyperparameter search 8x8/qmix/qmix_8x8_hs_2'
    # path2 = 'C:/Users/Wintermute/Desktop/hyperparameter search 8x8/qmix/qmix_8x8_hs_realone'
    base_path = 'C:/Users/Wintermute/Desktop/hyperparameter search 8x8'
    path1 = 'C:/Users/Wintermute/Desktop/hyperparameter search 8x8/vdn/vdn_8x8_hs'
    path2 = 'C:/Users/Wintermute/Desktop/hyperparameter search 8x8/vdn/vdn_8x8_hs_2'
    
    copy_folder(path1, path2)


if __name__ == '__main__':
    _main()