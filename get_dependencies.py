import importlib
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
