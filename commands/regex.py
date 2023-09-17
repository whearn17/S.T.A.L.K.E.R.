def regex(shell_instance, pattern):
    """Searches for files that match the given regex pattern in their filenames."""
    if not pattern:
        print("Please provide a regex pattern to search for.")
        return

    # Use the regex pattern to filter filenames
    matching_files = shell_instance.df[
        shell_instance.df['FileName'].str.contains(pattern, case=False, na=False, regex=True)]

    if matching_files.empty:
        print(f"No files matching the regex pattern '{pattern}' were found.")
        return

    print(f"Files matching the regex pattern '{pattern}':")
    for _, row in matching_files.iterrows():
        print(row['FileName'])
