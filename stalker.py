import pandas as pd
import cmd


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

    def do_mfilechanges(self, arg):
        """Show the top 10 days with the most file changes"""
        date_counts = self.df['LastRecordChange0x10'].dt.date.value_counts()
        top_10_dates = date_counts.head(10)

        print("Top 10 days with the most file changes:")
        for date, count in top_10_dates.items():
            print(f"{date}: {count} file changes")

    def do_fdupes(self, arg):
        """List the top 10 files that appear more than once, sorted by their frequency"""
        duplicates = self.df['FileName'].value_counts()
        duplicates = duplicates[duplicates > 1].sort_values(ascending=False).head(10)

        print("Top 10 most commonly repeated files:")
        for filename, count in duplicates.items():
            print(f"{filename}: {count} times")

    def do_rexec(self, arg):
        """Find all executables with their "Created0x10" or "Created0x30" matching the given date.

        Usage: find_executables_by_date YYYY-MM-DD
        """
        if not arg:
            print("Please provide a date in the format YYYY-MM-DD.")
            return

        # Parse the date
        try:
            search_date = pd.to_datetime(arg).date()
        except ValueError:
            print("Invalid date format. Please provide a date in the format YYYY-MM-DD.")
            return

        # Filter data based on the provided date and executable extensions
        condition = (
                ((self.df['Created0x10'].dt.date == search_date) | (self.df['Created0x30'].dt.date == search_date)) &
                (self.df['FileName'].str.endswith(('.exe', '.vba', '.bat', '.cmd', '.ps1', '.msi')))
        )

        executables = self.df[condition]

        if executables.empty:
            print(f"No executables found on {search_date}.")
            return

        print(f"Executables found on {search_date}:")
        for _, row in executables.iterrows():
            print(row['FileName'])

    def do_ffrf(self, file_extension):
        """Find the first ten files by Created0x10 for a given file extension.

        Usage: ffrf .ext
        """
        if not file_extension:
            print("Please provide a file extension (e.g., .exe, .dll).")
            return

        # Filter out rows where FileName is NaN
        valid_names_df = self.df[self.df['FileName'].notna()]

        # Filter the dataframe by the given file extension
        filtered_df = valid_names_df[valid_names_df['FileName'].str.endswith(file_extension)]

        # Sort the filtered dataframe by Created0x10
        sorted_df = filtered_df.sort_values(by='Created0x10')

        # Select the first ten rows
        top_ten = sorted_df.head(10)

        if top_ten.empty:
            print(f"No files with the {file_extension} extension found.")
            return

        print(f"First ten {file_extension} files sorted by Created0x10:")
        for _, row in top_ten.iterrows():
            print(f"{row['FileName']} - {row['Created0x10']}")

    @staticmethod
    def do_exit(self, arg):
        """Exit the shell"""
        return True


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print("Usage: stalker.py <path_to_mft_csv_file>")
        sys.exit(1)

    shell = MFTShell(sys.argv[1])
    shell.cmdloop("Welcome to the MFT interactive shell. Type 'help' for a list of commands.")
