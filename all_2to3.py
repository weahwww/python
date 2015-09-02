import os

if __name__ == "__main__":
	tool = "C:\\Python34\\Tools\\Scripts\\2to3.py"

	top_dir = os.path.split(os.path.realpath(__file__))[0]

	for dir_path,subpaths,files in os.walk(top_dir,False):
		for filename in files:
			if filename[-2:] == "py":
				fullname = os.path.join(dir_path,filename)
				os.system("python {0} -w {1}".format(tool, fullname))
