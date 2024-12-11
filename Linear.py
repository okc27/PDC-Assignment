import csv
from datetime import datetime
from collections import defaultdict

# Record start time
start_time = datetime.now()

# Placeholder year (assume current year for simplicity)
current_year = datetime.now().year

# Load student data into std_data
with open('students.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    std_data = list(reader)

# Load fees data into fees_data and organize by Student ID
fees_by_student = defaultdict(list)
with open('student_fees.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for fee in reader:
        try:
            if fee["Fee Status"].strip().lower() == "paid":
                # Convert "Month Day" format to a full date with a default year
                fee_date = datetime.strptime(f"{fee['Payment Date']} {current_year}", "%B %d %Y")
                fees_by_student[fee["Student ID"].strip()].append(fee_date)
        except ValueError as e:
            print(f"Skipping invalid date: {fee['Payment Date']} - Error: {e}")

# Debug: Check fees_by_student content
print("Sample Fees Data (by Student ID):", dict(list(fees_by_student.items())[:5]))

# List for storing output
output_data = []

# Process each student
for student in std_data:
    stud_id = student["Student ID"].strip()  # Ensure no extra spaces
    student_fee_dates = fees_by_student.get(stud_id, [])

    if student_fee_dates:
        # Find the most frequent fee submission day of the month
        day_frequencies = defaultdict(int)
        for date in student_fee_dates:
            day_of_month = date.day  # Extract day of the month (1, 2, 3, ...)
            day_frequencies[day_of_month] += 1

        # Find the day with the highest frequency
        max_day = max(day_frequencies, key=day_frequencies.get)
        max_frequency = day_frequencies[max_day]

        # Append result to output_data
        output_data.append({
            "Student ID": stud_id,
            "Most Frequent Fee Submission Day": max_day,
            "Frequency": max_frequency
        })

# Debug: Check if output_data is populated
print("Output Data Sample:", output_data[:5])

# Write output_data to a CSV file
output_file = 'most_frequent_fee_days.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    fieldnames = ["Student ID", "Most Frequent Fee Submission Day", "Frequency"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output_data)

# Record end time
end_time = datetime.now()

# Calculate total execution time
execution_time = end_time - start_time

# Display results
print("Execution Results:")
for entry in output_data:
    print(f"Student ID: {entry['Student ID']}, "
          f"Most Frequent Day: {entry['Most Frequent Fee Submission Day']}, "
          f"Frequency: {entry['Frequency']}")

# Display execution times
print("\nExecution Timing:")
print(f"Start Time: {start_time}")
print(f"End Time: {end_time}")
print(f"Total Execution Time: {execution_time}")
