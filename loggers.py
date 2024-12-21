from datetime import timezone, timedelta, datetime
from pathlib import Path

KST = timezone(timedelta(hours=9))



class Logger:
    work_path: Path

    def dt(self):
        return datetime.now(self.KST)

    def __init__(self, log_filepath, *args, **kwargs):
        self.log_filepath = log_filepath
        self.log_filepath.parent.mkdir(exist_ok=True)
        self.KST = timezone(timedelta(hours=9))

    def add_log(self, msg: str):

        with open(self.log_filepath, 'at') as fout:
            s = f'[{self.dt().strftime("%Y-%m-%d %H:%M:%S")}] {msg}'
            print(s)
            fout.write(f'{s}\n')
