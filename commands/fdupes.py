def fdupes(shell_instance, arg):
    """List the top 10 files that appear more than once, sorted by their frequency"""
    duplicates = shell_instance.df['FileName'].value_counts()
    duplicates = duplicates[duplicates > 1].sort_values(ascending=False).head(10)

    print("Top 10 most commonly repeated files:")
    for filename, count in duplicates.items():
        print(f"{filename}: {count} times")
