import sys
import json
import copy
from datetime import timedelta, datetime


dur = [0, 1]
for i in range(20):
    dur.append(dur[-1] + dur[-2])

date_format = '%Y/%m/%d'
datetime_format = '%Y/%m/%d %H:%M:%S'


def main():
    idata = json.loads(sys.stdin.read())
    odata = []
    for icard in idata:
        ocard = copy.copy(icard)
        stage = ocard.pop('stage')
        ask_date = ocard.pop('ask_date')
        ask_date = datetime.strptime(ask_date, date_format)
        pask_date = ask_date - timedelta(dur[stage])
        if stage > 0:
            stage -= 1
        ppask_date = pask_date - timedelta(dur[stage])

        ocard['ask_date'] = ask_date.strftime(datetime_format)
        ocard['pask_date'] = pask_date.strftime(datetime_format)
        ocard['ppask_date'] = ppask_date.strftime(datetime_format)
        odata.append(ocard)
    print(json.dumps(odata))
    return 0


if __name__ == '__main__':
    exit(main())
