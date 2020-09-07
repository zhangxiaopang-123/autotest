

import yaml,os,json
from services import config


def read_():
    basedir = config.basedir
    data_path = os.path.join(basedir, 'config/wbf.yaml')
    with open(data_path, 'r', encoding='utf-8') as f:
        d = yaml.safe_load(f.read())
        # print(d)
        return d
        # print(json.dumps(d['user'],indent=2,sort_keys=True,separators=(',',':')))
        # print(d['test-5']['user'].split(',')[0])


if __name__ == '__main__':
    read_()

