import sys
sys.path.insert(1, './Library/scripts')

from RTIMUScripts import get_heading

while True:
    print(str(get_heading()))
