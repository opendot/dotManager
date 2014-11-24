from distutils.core import setup
import py2exe

setup(
    windows = [{
            "script":"main.py",
            "icon_resources": [(1, "icon.ico")],
            "dest_base":"dot Manager"
            }],
)
