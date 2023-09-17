def mfilechanges(shell_instance, arg):
    """Show the top 10 days with the most file changes"""
    date_counts = shell_instance.df['LastRecordChange0x10'].dt.date.value_counts()
    top_10_dates = date_counts.head(10)

    print("Top 10 days with the most file changes:")
    for date, count in top_10_dates.items():
        print(f"{date}: {count} file changes")
