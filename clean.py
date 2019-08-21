"""Delete Python cache and Pytest cache folders completely"""

import pathlib
import shutil

for p in pathlib.Path('.').rglob('__pycache__'):
    shutil.rmtree(p)
for p in pathlib.Path('.').rglob('.pytest_cache'):
    shutil.rmtree(p)
