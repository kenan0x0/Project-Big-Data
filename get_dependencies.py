import importlib

# Important notes! This program requires the latest versions of all three browsers to be installed on the host machine. All browsers must have selenium webdrivers with them
# All libraries below must be present and the python interpreter must be 3.8 and higher otherwise terminating processes won't work.

# 1. Latest versions of browsers
# 2. Matching versions for the selenium webdrivers of the adforementioned brwosers
# 3. Python environment 3.9 and higher
deps = ["flask", "multiprocessing", "psutil", "pickle", "pandas", "sqlalchemy", "time", "ssl", "smtplib", "selenium", "bs4", "msedge-selenium-tools", "requests"]

counter = 1

for package in deps:
    try:
        importlib.import_module(package)
        print(str(counter) + ". " + str(package) + " Found!\n")
        counter += 1
    except ImportError:
        print(str(counter) + ". " + str(package)+ " Is missing.. Downloading\n")
        import pip
        pip.main(['install', package])
        counter += 1
