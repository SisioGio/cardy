import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))
from handler import lambda_handler


print(lambda_handler({},{}))

