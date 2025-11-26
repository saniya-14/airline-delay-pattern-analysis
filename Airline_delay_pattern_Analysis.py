import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set plot style
sns.set(style="whitegrid")

# Load the dataset
df = pd.read_csv('data.csv')

# Clean Flight Price
df['Flight Price'] = df['Flight Price'].astype(str)
df['Flight Price'] = df['Flight Price'].str.replace('"', '', regex=False)
df['Flight Price'] = df['Flight Price'].str.replace(',', '', regex=False)
df['Flight Price'] = pd.to_numeric(df['Flight Price'], errors='coerce')

# Clean Duration Time (convert to minutes)
duration_list = []
for d in df['Duration Time']:
    d = str(d).strip()
    if 'h' in d and 'm' in d:
        h, m = d.split('h')
        total = int(h.strip()) * 60 + int(m.strip()[:-1])
    elif 'h' in d:
        total = int(d.strip()[:-1]) * 60
    elif 'm' in d:
        total = int(d.strip()[:-1])
    else:
        total = 0
    duration_list.append(total)

df['Duration (min)'] = duration_list

# Convert Departure and Arrival Time
df['Departure Time'] = pd.to_datetime(df['Departure Time'].str.strip(), format='%H:%M', errors='coerce').dt.time
df['Arrival Time'] = pd.to_datetime(df['Arrival Time'].str.strip(), format='%H:%M', errors='coerce').dt.time

# Convert Date
df['Date'] = pd.to_datetime(df['Date'].str.strip(), format='%d-%m-%Y', errors='coerce')

# Clean Cabin Class
df['Cabin Class'] = df['Cabin Class'].str.strip()

# Create delay column
df['Delayed'] = df['Duration (min)'] > 120

#PLOTTING SECTION

# 1. Bar plot: Delay count per airline
plt.figure(figsize=(8, 5))
delay_counts = df.groupby('Company')['Delayed'].sum()
sns.barplot(x=delay_counts.index, y=delay_counts.values, palette='pastel')
plt.title('Flight Delays by Airline')
plt.xlabel('Airline')
plt.ylabel('Number of Delayed Flights')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('Flight Delay')
plt.show()

# 2. Box plot: Price distribution per airline
plt.figure(figsize=(10, 5))
sns.boxplot(data=df, x='Company', y='Flight Price', palette='Set2')
plt.title('Flight Price Distribution by Airline')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('Flight Price Distribution')
plt.show()

# 3. Histogram: Flight Duration Distribution
plt.figure(figsize=(8, 5))
sns.histplot(df['Duration (min)'], bins=20, kde=True, color='coral')
plt.title('Flight Duration Distribution')
plt.xlabel('Duration (minutes)')
plt.ylabel('Number of Flights')
plt.tight_layout()
plt.savefig('Flight Duration Distribution')
plt.show()

# 4. Count plot: Delayed vs On-Time flights
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x='Delayed', palette='coolwarm')
plt.title('Flight Delays vs On-Time')
plt.xticks([0, 1], ['On-Time', 'Delayed'])
plt.ylabel('Number of Flights')
plt.tight_layout()
plt.savefig('Flight Delays vs On-Time')
plt.show()

# 5. Line plot: Average Duration over Dates
avg_duration = df.groupby('Date')['Duration (min)'].mean().reset_index()
plt.figure(figsize=(10, 5))
sns.lineplot(data=avg_duration, x='Date', y='Duration (min)', marker='o', color='green')
plt.title('Average Flight Duration Over Time')
plt.xlabel('Date')
plt.ylabel('Average Duration (min)')
plt.tight_layout()
plt.savefig('Average Flight Duration Over Time')
plt.show()

# Export cleaned data
df.to_csv("cleaned_flight_data.csv", index=False)
print("Cleaned data saved to cleaned_flight_data.csv")