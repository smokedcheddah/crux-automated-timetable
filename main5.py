import mysql.connector
import random
import matplotlib.pyplot as plt
import pandas as pd








connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1511",
    database="schedu_db"
)

if connection.is_connected():
    print("Connection successful!")
else:
    print("Connection failed!")

cursor = connection.cursor(dictionary=True)
cursor.execute("SELECT * FROM teacher_schedulez")
subjects = cursor.fetchall()


CHEMF110_slots = []
CHEMF111_slots = []
CHEMTF111_slots = []
EEEF111_slots = []
EEETF111_slots = []
MEF112L_slots = []
PHYF111_slots = []
PHYTF111_slots = []
MATHF111_slots = []
MATHTF111_slots = []
MEF112_slots = []
PHYF110_slots = []

subject_list = {
    'CHEM F111': CHEMF111_slots,
    'CHEM F110': CHEMF110_slots,
    'EEE F111': EEEF111_slots,
    'ME F112': MEF112_slots,
    'PHY F111': PHYF111_slots,
    'MATH F111': MATHF111_slots,
    'PHY TF111': PHYTF111_slots,
    'MATH TF111': MATHTF111_slots,
    'EEE TF111': EEETF111_slots,
    'CHEM TF111': CHEMTF111_slots,
    'ME F112 LEC': MEF112L_slots,
    'PHY F110': PHYF110_slots,
}


for subject in subjects:
    if subject['subject_name'] in subject_list:
        subject_list[subject['subject_name']].append(subject)






for subject, slots in subject_list.items():
    print(f"{subject}: {len(slots)} slots available")



def check_conflict(selected_slots):
    slots = set()
    for slot in selected_slots:
        if (slot['day'], slot['time_slot']) in slots:
            return True  # Conflict found
        slots.add((slot['day'], slot['time_slot']))
    return False  # No conflict



def select_slots(subject_list):
    while True:
        selected_slots = []
        for subject, slots in subject_list.items():
            if not slots:
                print(f"Error: No available slots for {subject}")
                return None

            selected_teacher = random.choice(slots)['teacher_name']
            for slot in slots:
                if slot['teacher_name'] == selected_teacher:
                    selected_slots.append(slot)

        if not check_conflict(selected_slots):
            return selected_slots



selected_slots = select_slots(subject_list)

if selected_slots:
    for slot in selected_slots:
        print(
            f"Subject: {slot['subject_name']}, Teacher: {slot['teacher_name']}, Day: {slot['day']}, Time: {slot['time_slot']}")
else:
    print("No valid schedule could be generated.")


df = pd.DataFrame(selected_slots)

day_order = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]

# Pivot the data to get days as columns and times as rows, with the correct day order
calendar = df.pivot(index='time_slot', columns='day', values='subject_name').reindex(columns=day_order)

# Plot the calendar
fig, ax = plt.subplots()
ax.axis('tight')
ax.axis('off')
table = ax.table(cellText=calendar.values, colLabels=calendar.columns, rowLabels=calendar.index, cellLoc='center', loc='center')

plt.show()



