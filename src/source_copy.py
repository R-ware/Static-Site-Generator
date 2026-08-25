import os
import shutil

def source_copy(static, public):
    if os.path.exists(static) == False:
        raise Exception("Static Folder Does Not Exist!")
    if os.path.exists(public):
        shutil.rmtree(public)
    os.mkdir(public)
    static_dir = os.listdir(static)
    for files in static_dir:
        static_path = os.path.join(static, files)
        public_path = os.path.join(public, files)
        if os.path.isfile(static_path):
            print(static_path," -> ", public_path)
            shutil.copy(static_path, public_path)
        else:
            source_copy(static_path, public_path)