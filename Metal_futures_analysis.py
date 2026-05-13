# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 12:15:01 2025

@author: pavitra
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

file_path = (r"C:\Users\pavitra\Downloads\Project Data set\data_set (1).xlsx")
all_sheets = pd.read_excel(file_path,sheet_name=None)
print(all_sheets)

print("Available sheet names:")
print(all_sheets.keys())

data_dict = {
    'copper_futures_data': all_sheets['copper_futures_data'],
    'silver_futures_data': all_sheets['silver_futures_data'],
    'gold_futures_data': all_sheets['gold_futures_data'],
    'platinum_futures_data': all_sheets['platinum_futures_data'],
    'palladium_futures_data': all_sheets['palladium_futures_data'],
    'aluminum_futures_data': all_sheets['aluminum_futures_data'],
    'zinc_futures_data': all_sheets['zinc_futures_data'],
    'steel_futures_data': all_sheets['steel_futures_data']
}

combined_data = pd.concat(
    [df.assign(Metal=Metal.replace('_futures_data', '')) for Metal, df in data_dict.items()],ignore_index=True)
combined_data.to_excel('Combined_metal_futures.xlsx', index=False)




# Convert to datetime with UTC timezone (if needed)
combined_data['Date'] = pd.to_datetime(combined_data['Date'], errors='coerce', utc=True)

# Remove timezone info to make it Excel-compatible
combined_data['Date'] = combined_data['Date'].dt.tz_localize(None)


# Convert price columns to float
price_columns = ['Open', 'High', 'Low', 'Close']
for col in price_columns:
    combined_data[col] = pd.to_numeric(combined_data[col], errors='coerce')


# Convert 'Volume' to int (handle NaNs if needed)
combined_data['Volume'] = pd.to_numeric(combined_data['Volume'], errors='coerce').astype('Int64')


# Convert 'Metal' to category
combined_data['Metal'] = combined_data['Metal'].astype('category')

print(combined_data.dtypes)




null_counts = combined_data.isnull().sum()
print(null_counts)


combined_data = combined_data.replace(r'^\s*$', np.nan, regex=True)
print("Before dropping NaNs:", combined_data.shape)

combined_df = combined_data.dropna()
print("After dropping NaNs:", combined_df.shape)

null_counts = combined_df.isnull().sum()
print(null_counts)




print(combined_df['Metal'].unique())
print(combined_df.head())
print(combined_df.shape)
print(combined_df.dtypes)
print(combined_df.describe())
print(combined_df.isnull().sum())
print(combined_df.duplicated().sum())


combined_df.to_csv('combined_all_metal_futures.csv', index=False)


# statistical analysis
# first moment of business
combined_df.groupby('Metal')[['Open','High','Low','Close','Volume']].mean()
combined_df.groupby('Metal')[['Open','High','Low','Close','Volume']].median()
combined_df.groupby('Metal')[['Open', 'High', 'Low', 'Close','Volume']].agg(lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan)


# second moment of business
combined_df.groupby('Metal')[['Open','High','Low','Close','Volume']].var()
combined_df.groupby('Metal')[['Open','High','Low','Close']].var()
combined_df.groupby('Metal')[['Open','High','Low','Close','Volume']].std()
combined_df.groupby('Metal')[['Open', 'High', 'Low', 'Close','Volume']].agg(lambda x: x.max() - x.min())

# 3rd Moment – Skewness
combined_df.groupby('Metal')[['Open','High','Low','Close','Volume']].skew()

#  4th Moment – Kurtosis
combined_df.groupby('Metal')[['Open','High','Low','Close','Volume']].apply(pd.DataFrame.kurt)


"Boxplot of Copper for all prices and volume"

def plot_copper_boxplots_all_in_one(df):
    # Filter only copper data
    copper_df = df[df['Metal'] == 'copper']

    # Select numeric columns
    numeric_columns = copper_df.select_dtypes(include='number').columns

    # Set up subplots
    num_cols = len(numeric_columns)
    fig, axes = plt.subplots(1, num_cols, figsize=(5 * num_cols, 5))

    # Plot each numeric column in its subplot
    for i, col in enumerate(numeric_columns):
        sns.boxplot(y=copper_df[col], ax=axes[i])
        axes[i].set_title(f"{col}")

    plt.tight_layout()
    plt.suptitle("Boxplots for Copper Data", fontsize=16, y=1.05)
    plt.show()

# Run it
plot_copper_boxplots_all_in_one(combined_df)





"Boxplot for each Metal on close price"

metals = combined_df['Metal'].unique()

for metal in metals:
    plt.figure(figsize=(7, 6))
    metal_df = combined_df[combined_df['Metal'] == metal]

    sns.boxplot(y=metal_df['Close'], color='green')
    plt.title(f'Boxplot of Close Price - {metal}')
    plt.ylabel('Close price')
    plt.tight_layout()
    plt.show()




"Boxplot of all metals on all prices and volume"

"Boxplot of all metals for detecting Outliers and for Comparision"

def plot_boxplots_by_metal(df):
    columns_to_plot = ['Open', 'High', 'Low', 'Close', 'Volume']

    for col in columns_to_plot:
        plt.figure(figsize=(10, 5))
        sns.boxplot(x='Metal', y=col, data=df)
        plt.title(f"Boxplot of {col} by Metal")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

plot_boxplots_by_metal(combined_df)







"Histogram of each Metal on Close price"

# Plot histograms for each metal
for metal in metals:
    plt.figure(figsize=(8, 5))
    metal_data = combined_df[combined_df['Metal'] == metal]['Close']
    
    plt.hist(metal_data, bins=30, color='blue', edgecolor='black', alpha=0.7)
    plt.title(f'Histogram of Close Prices - {metal}')
    plt.xlabel('Close Price')
    plt.ylabel('Frequency')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()





"Line chart of copper with all prices and volume"

# Filter for Copper data only
copper_df = combined_df[combined_df['Metal'] == 'copper']

# List of columns to plot
columns_to_plot = ['Open', 'High', 'Low', 'Close', 'Volume']

# Loop through each column and plot a separate line chart
for col in columns_to_plot:
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=copper_df, x='Date', y=col, color='black')  # Change color if needed
    plt.title(f"{col} Price Trend - Copper")
    plt.xlabel("Date")
    plt.ylabel(f"{col} Price")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()





"line chart visualization for comparision with all metals"

metals_to_compare = ['copper', 'silver', 'gold', 'platinum', 'palladium', 'aluminum', 'zinc', 'steel']  # Pick the ones you want
compare_df = combined_df[combined_df['Metal'].isin(metals_to_compare)]

plt.figure(figsize=(10, 6))
sns.lineplot(data=compare_df, x='Date', y='Close', hue='Metal')
plt.title("Close Price Trend: Copper vs Other Metals")
plt.xlabel("Date")
plt.ylabel("Close Price")
plt.legend(title='Metal')
plt.tight_layout()
plt.show()








"Scatter plot of copper, comparision  all prices"

fig, axs = plt.subplots(2, 3, figsize=(15, 10))

# Scatter Plot 1: Open vs Close
axs[0, 0].scatter(combined_df['Open'], combined_df['Close'], alpha=0.8)
axs[0, 0].set_xlabel('Open Price')
axs[0, 0].set_ylabel('Close Price')
axs[0, 0].set_title('Open vs Close')

# Scatter Plot 2: Open vs High
axs[0, 1].scatter(combined_df['Open'], combined_df['High'], alpha=0.8)
axs[0, 1].set_xlabel('Open Price')
axs[0, 1].set_ylabel('High Price')
axs[0, 1].set_title('Open vs High')

# Scatter Plot 3: Open vs Low
axs[0, 2].scatter(combined_df['Open'], combined_df['Low'], alpha=0.8)
axs[0, 2].set_xlabel('Open Price')
axs[0, 2].set_ylabel('Low Price')
axs[0, 2].set_title('Open vs Low')

# Scatter Plot 4: Close vs High
axs[1, 0].scatter(combined_df['Close'], combined_df['High'], alpha=0.8)
axs[1, 0].set_xlabel('Close Price')
axs[1, 0].set_ylabel('High Price')
axs[1, 0].set_title('Close vs High')

# Scatter Plot 5: Close vs Low
axs[1, 1].scatter(combined_df['Close'], combined_df['Low'], alpha=0.8)
axs[1, 1].set_xlabel('Close Price')
axs[1, 1].set_ylabel('Low Price')
axs[1, 1].set_title('Close vs Low')

# Scatter Plot 6: High vs Low
axs[1, 2].scatter(combined_df['High'], combined_df['Low'], alpha=0.8)
axs[1, 2].set_xlabel('High Price')
axs[1, 2].set_ylabel('Low Price')
axs[1, 2].set_title('High vs Low')

# Adjust layout for better spacing
plt.tight_layout()

# Show the plots
plt.show()




"Scatter plot of all Metal for comparision"

# Set up the plot
plt.figure(figsize=(10, 8))

# Loop through each metal and plot on the same axes
for metal in combined_df['Metal'].unique():
    metal_data = combined_df[combined_df['Metal'] == metal]
    plt.scatter(metal_data['Date'], metal_data['Close'], label=metal, s=10, alpha=0.6)

# Add plot details
plt.title('Close Prices Over Time by Metal')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.legend(title='Metal')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()







"Correlation analysis of all metal on close price"

pivot_close = combined_df.pivot(index='Date', columns='Metal', values='Close').dropna()
corr_matrix = pivot_close.corr()

# Plot the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, square=True)

# Styling
plt.title("Correlation Matrix of Metal Close Prices", fontsize=14)
plt.tight_layout()
plt.show()




"Correlation analysis in copper based on all prices"

copper_df = combined_df[combined_df['Metal'] == 'copper']

# Correlation matrix
copper_corr = copper_df[['Open', 'High', 'Low', 'Close']].corr()

# Heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(copper_corr, annot=True, cmap='YlGnBu', linewidths=0.5)
plt.title('Correlation Heatmap: Copper')
plt.show()








"Bar chart visualization on Average close price by metal"

avg_close = combined_df.groupby('Metal')['Close'].mean().sort_values(ascending=False)

# Plot bar chart
plt.figure(figsize=(10, 6))
avg_close.plot(kind='bar', color='green', edgecolor='black')

# Add labels and title
plt.title('Average Close Price by Metal')
plt.xlabel('Metal')
plt.ylabel('Average Close Price')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()




'''Scatter plot of Copper based on comparision with all prices'''

plt.scatter(combined_df['Open'], combined_df['Close'], alpha=0.8)
plt.xlabel('Open Price')
plt.ylabel('Close Price')
plt.title('Scatter Plot: Open vs Close')
plt.show()



plt.scatter(combined_df['Open'], combined_df['High'], alpha=0.8)
plt.xlabel('Open Price')
plt.ylabel('High Price')
plt.title('Scatter Plot: Open vs High')
plt.show()


plt.scatter(combined_df['Open'], combined_df['Low'], alpha=0.8)
plt.xlabel('Open Price')
plt.ylabel('Low Price')
plt.title('Scatter Plot: Open vs Low')
plt.show()



plt.scatter(combined_df['Close'], combined_df['High'], alpha=0.8)
plt.xlabel('Close Price')
plt.ylabel('High Price')
plt.title('Scatter Plot: Close vs High')
plt.show()



plt.scatter(combined_df['Close'], combined_df['Low'], alpha=0.8)
plt.xlabel('Close Price')
plt.ylabel('Low Price')
plt.title('Scatter Plot: Close vs Low')
plt.show()



plt.scatter(combined_df['High'], combined_df['Low'], alpha=0.8)
plt.xlabel('High Price')
plt.ylabel('Low Price')
plt.title('Scatter Plot: High vs Low')
plt.show()





"discrete data scatter plot"
combined_df['Metal'].value_counts().plot(kind='bar', color='green')
plt.title('Count of Records by Metal')
plt.xlabel('Metal')
plt.ylabel('Count')
plt.show()



