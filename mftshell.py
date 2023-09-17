import pandas as pd
import cmd
from commands import *


class MFTShell(cmd.Cmd):
    prompt = 'MFT> '

    def __init__(self, file_path):
        super().__init__()
        self.df = self.load_mft_file(file_path)

    @staticmethod
    def load_mft_file(file_path):
        df = pd.read_csv(file_path, low_memory=False)
        df['LastRecordChange0x10'] = pd.to_datetime(df['LastRecordChange0x10'])
        df['Created0x10'] = pd.to_datetime(df['Created0x10'], errors='coerce')
        df['Created0x30'] = pd.to_datetime(df['Created0x30'], errors='coerce')
        return df

    # your logic here

    def do_mfilechanges(self, arg):
        return mfilechanges(self, arg)

    def do_fdupes(self, arg):
        return fdupes(self, arg)

    def do_rexec(self, arg):
        return rexec(self, arg)

    def do_ffrf(self, file_extension):
        return ffrf(self, file_extension)

    @staticmethod
    def do_exit(arg):
        return True
