import matplotlib.pyplot as plt
import numpy as np

# Assuming 'dat' is a list of SGPA values in alphabets
dat = ['F', 'C', 'A+', 'D', 'O']  # Example data

# List of alphabet grades in ascending order (lowest grade first)
alphabet_grades = ['F', 'D', 'C', 'B', 'B+', 'A', 'A+', 'O']

# Convert alphabet SGPA values to their corresponding indices
data = {}
co = 1
subjects=["c","python","java","python web development","dsa"]
for i in range(len(dat)):
    key = subjects[i]
    value = alphabet_grades.index(dat[i]) + 1  # +1 to make the range 1-8
    data[key] = value
    co += 1
print(data)

courses = list(data.keys())
values = list(data.values())

fig, ax = plt.subplots(figsize=(8, 5))

# Defining bar positions
bar_width = 0.5
bar_positions = np.arange(len(courses))

# Creating the vertical bar plot with reduced width and closer spacing
bars = ax.bar(bar_positions, values, width=bar_width)
ax.set_xlabel("Semesters")
ax.set_ylabel("Grades")
ax.set_title("Grades per Semester")

# Set y-ticks to be alphabet grades
numeric_range = np.arange(1, len(alphabet_grades) + 1)

# Adding custom alphabet labels
ax.set_yticks(numeric_range)
ax.set_yticklabels(alphabet_grades)

# Adding values on the bars with increased font size
for bar, grade in zip(bars, dat):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), grade, 
            ha='center', va='bottom', fontsize=12, weight='bold')

# Setting x-ticks to be in the center of the bars
ax.set_xticks(bar_positions)
ax.set_xticklabels(courses)

# Changing the figure title
fig.suptitle("Grades ", fontsize=16, fontweight='bold')

# Display the plot
plt.show()
