def ffrf(shell_instance, file_extension):
    """Find the first ten files by Created0x10 for a given file extension.

    Usage: ffrf .ext
    """
    if not file_extension:
        print("Please provide a file extension (e.g., .exe, .dll).")
        return

    # Filter out rows where FileName is NaN
    valid_names_df = shell_instance.df[shell_instance.df['FileName'].notna()]

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
