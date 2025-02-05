import sys

srcPath = ["..YourDirPath.. + /SH_tools"]

for _path in srcPath:
    if _path not in sys.path:
        sys.path.append(_path)
    for i in sys.path:
        print(i)

try:
    reload(SH)
    reload(SH_tools_Run)
except:
	import SH_script as SH
	import SH_tools_Run

try:
    SH_ui.close()
    SH_ui.deleteLater()
except:
    pass

SH_ui = SH_tools_Run.DesignerUI()
SH_ui.show()