import pandas as pd


def rexec(shell_instance, arg):
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
            ((shell_instance.df['Created0x10'].dt.date == search_date) | (
                    shell_instance.df['Created0x30'].dt.date == search_date)) &
            (shell_instance.df['FileName'].str.endswith(('.exe', '.vba', '.bat', '.cmd', '.ps1', '.msi')))
    )

    executables = shell_instance.df[condition]

    if executables.empty:
        print(f"No executables found on {search_date}.")
        return

    print(f"Executables found on {search_date}:")
    for _, row in executables.iterrows():
        print(row['FileName'])
