import pandas as pd
from datetime import datetime

# Record start time
start_time = datetime.now()

# Placeholder year (assume current year for simplicity)
current_year = datetime.now().year

# Load students and fees data into Pandas DataFrames
students_df = pd.read_csv('students.csv', encoding='utf-8')
fees_df = pd.read_csv('student_fees.csv', encoding='utf-8')

# Ensure "Fee Status" is processed correctly
fees_df['Fee Status'] = fees_df['Fee Status'].str.strip().str.lower()

# Convert "Payment Date" from "Month Day" to a complete date with year
fees_df['Payment Date'] = fees_df['Payment Date'] + f" {current_year}"
fees_df['Payment Date'] = pd.to_datetime(fees_df['Payment Date'], format='%B %d %Y', errors='coerce')

# Filter only paid fees
paid_fees = fees_df[fees_df['Fee Status'] == 'paid']

# Extract the day of the month
paid_fees['Day of Month'] = paid_fees['Payment Date'].dt.day

# Group by Student ID and Day of Month to count occurrences
day_frequency = paid_fees.groupby(['Student ID', 'Day of Month']).size().reset_index(name='Frequency')

# Find the most frequent day for each student
most_frequent_days = day_frequency.loc[
    day_frequency.groupby('Student ID')['Frequency'].idxmax()
]

# Merge the most frequent day data with the student data
output_data = students_df.merge(
    most_frequent_days[['Student ID', 'Day of Month', 'Frequency']],
    on='Student ID',
    how='left'
)

# Write output_data to a CSV file
output_file = 'most_frequent_fee_days.csv'
output_data.to_csv(output_file, index=False, encoding='utf-8')

# Record end time
end_time = datetime.now()

# Calculate total execution time
execution_time = end_time - start_time

# Display results
print("Execution Results:")
print(output_data[['Student ID', 'Day of Month', 'Frequency']])

# Display execution times
print("\nExecution Timing:")
print(f"Start Time: {start_time}")
print(f"End Time: {end_time}")
print(f"Total Execution Time: {execution_time}")
