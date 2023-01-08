import argparse

from t2 import *

os.environ['KMP_DUPLICATE_LIB_OK']='True' 

parser = argparse.ArgumentParser()
parser.add_argument("--pipeline_dir", type=str, dest="pipeline_dir")
parser.add_argument("--input_dir", type=str, dest="input_dir")
parser.add_argument("--batch_size", default=1, type=int, dest="batch_size")

parser.add_argument('--opts', nargs='+', default=['direction', 1], dest='opts')
parser.add_argument("--nch", default=1, type=int, dest="nch")
parser.add_argument("--nker", default=64, type=int, dest="nker")

parser.add_argument("--norm", default='bnorm', type=str, dest="norm")
args = parser.parse_args()

test(args)
