import json
from amscommon import read_config

config = read_config()
print json.dumps(config, ensure_ascii=False, encoding="utf-8")
