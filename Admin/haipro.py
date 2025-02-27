import matplotlib.pyplot as plt
import numpy as np

# Data
data = [
    ['Lecturer Name', 'Subject Name', 'Subject Code', 'Total Strength', 
     'O', 'A+', 'A', 'B+', 'B', 
     'C', 'AB', 'M', 'F', 
     'Passed', 'Pass %'],
    
    ['Dr. K. Prakash', 'Mathematics', 'B20CS37', 125, 1, 18, 32, 33, 26, 13, 2, 0, 0, 123, 98],
    ['Dr. P. Sadanandam', 'Biology', 'B20CS36', 147, 0, 9, 39, 51, 33, 13, 2, 0, 0, 145, 98],
    ['Dr. K. Ranjith Kumar', 'Physics', 'B20AI10', 135, 0, 1, 25, 56, 38, 13, 2, 0, 0, 133, 98],
    ['Dr. Ch. Raju', 'Chemistry', 'B20CS39', 121, 0, 7, 34, 40, 19, 18, 3, 0, 0, 118, 97],
    ['T. Venugopal', 'History', 'B20MB03', 112, 0, 0, 1, 30, 77, 2, 2, 0, 0, 110, 98],
    ['B. Nagaraju', 'Literature', 'B20CS52',76 ,0 ,0 ,15 ,35 ,22 ,3 ,0 ,1 ,0 ,75 ,98]
]

# Extracting relevant data
subjects = [row[1] for row in data[1:]] # Skip header row
lecturers = [row[0] for row in data[1:]] # Extract lecturer names
grades = np.array([row[4:13] for row in data[1:]]) # Extract grades for each subject

# Set the width of the bars
bar_width = 0.1

# Set positions of bar groups on x-axis
x = np.arange(len(subjects))

# Create a figure and axis
fig, ax = plt.subplots(figsize=(12,6))

# Create bars for each grade
for i in range(grades.shape[1]):
    bars = ax.bar(x + i * bar_width , grades[:, i], width=bar_width,
                  label=data[0][4 + i]) # Using header names for labels
    
    # Add text annotations for each bar
    for j, bar in enumerate(bars):
        height = bar.get_height()
        # Display number of students
        ax.text(bar.get_x() + bar.get_width()/2 - bar_width/4,
                height,
                str(int(height)),
                ha='center',
                va='bottom',
                fontsize=8)

        # Display grade label above the number
        ax.text(bar.get_x() + bar.get_width()/2 - bar_width/4,
                height + (height * .05), # Offset to place grade above the number
                data[0][4 + i], # Grade label from header
                ha='center',
                va='bottom',
                fontsize=8)

# Add subject names and lecturer names with proper spacing to avoid overlap
for i in range(len(subjects)):
    ax.text(x[i] - bar_width/2 + (bar_width / len(grades))/2,
            -3.5,
            subjects[i], 
            ha='center',
            va='top',
            fontsize=10)
    
    ax.text(x[i] - bar_width/2 + (bar_width / len(grades))/2,
            -5,
            lecturers[i], 
            ha='center',
            va='top',
            fontsize=8)

# Adding labels and title
ax.set_xlabel('Subjects')
ax.set_ylabel('Number of Students')
ax.set_title('Grade Distribution by Subject')
ax.set_xticks(x)
ax.set_xticklabels(['' for _ in range(len(subjects))]) # Remove x-tick labels
ax.legend(title='Grades')

# Adjust spacing
plt.subplots_adjust(bottom=0.15) # Increase bottom margin for better visibility
plt.tight_layout()

# Show the plot
plt.show()