import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs("/output", exist_ok=True)
shutil.copyfile(os.path.join(HERE, "entry.png"), "/output/entry.png")
