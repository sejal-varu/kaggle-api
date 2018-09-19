import subprocess
import json
import os

dataset_meta_path = "datasets/dataset-metadata.json"
kernel_meta_path = "scripts/kernel-metadata.json"


def create_dataset(name):
	subprocess.call(["kaggle", "datasets", "init", "-p", "datasets/"])
	
	with open(dataset_meta_path, 'r', encoding='utf-8') as metaFile:
		metadata = json.load(metaFile)

	metadata["title"] = name
	metadata["id"] = metadata["id"].replace("INSERT_SLUG_HERE",name)
	with open(dataset_meta_path, "w") as metaFile:
		json.dump(metadata, metaFile)
	subprocess.call(["kaggle", "datasets", "create", "-p", "datasets/"])
	print("Dataset pushed")
	return metadata["id"]


def create_kernel(name,dataset_id):
	subprocess.call(["kaggle", "kernels", "init", "-p", "scripts/"])
	
	with open(kernel_meta_path, 'r', encoding='utf-8') as metaFile:
		metadata = json.load(metaFile)

	py_files = [f for f in os.listdir("scripts/") if f.endswith('.py')]
	metadata["title"] = "KERNEL_"+name
	metadata["id"] = metadata["id"].replace("INSERT_KERNEL_SLUG_HERE","kernel_"+name)
	metadata["code_file"] = py_files[0]
	metadata["language"] = "python"
	metadata["kernel_type"] = "script"
	metadata["dataset_sources"] = [dataset_id]

	with open(kernel_meta_path, "w") as metaFile:
		json.dump(metadata, metaFile)
	subprocess.call(["kaggle", "kernels", "push", "-p", "scripts/"])
	print("Kernel pushed")



name = input("Enter a name to dataset/kernel: ")	

dataset_id = create_dataset(name)
create_kernel(name,dataset_id)


