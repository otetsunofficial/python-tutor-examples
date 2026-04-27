import os, shutil
from pathlib import Path

base_path = Path(".")
target_dir = "test1/test2"
os.makedirs(target_dir, exist_ok=True)


file_path = os.path.join(target_dir, "find_me.txt")
with open(file_path, "x") as f:
    f.write("you found me")

found_files = list(base_path.rglob("*.txt"))
print(found_files)

shutil.move(file_path, ".")
shutil.move("./find_me.txt", file_path)

os.remove(file_path)
os.rmdir("test1/test2")
os.rmdir("test1")
