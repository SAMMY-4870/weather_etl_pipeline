def update(frame):
    """Update the bar chart in real time."""
    plt.cla()  # clear previous frame
    df = fetch_data()

    if df.empty:
        plt.title("No data available yet...")
        return

    bars = plt.bar(df["city"], df["temp_celsius"], color="skyblue", edgecolor="black")
    plt.title("Real-Time Temperature Comparison 🌡️", fontsize=14)
    plt.xlabel("City", fontsize=12)
    plt.ylabel("Temperature (°C)", fontsize=12)
    plt.ylim(0, max(df["temp_celsius"]) + 5)  # space for labels

    # Highlight max and min
    max_temp = df["temp_celsius"].max()
    min_temp = df["temp_celsius"].min()

    for bar in bars:
        height = bar.get_height()
        city = bar.get_x() + bar.get_width()/2
        plt.text(city, height+0.5, f"{height}°C", ha="center", fontsize=10)

        if height == max_temp:
            bar.set_color("red")
        elif height == min_temp:
            bar.set_color("blue")
