from uwaterloo import *
import os

print(len(UWaterloo(os.environ['UW_API_KEY{}']).get_courses()))