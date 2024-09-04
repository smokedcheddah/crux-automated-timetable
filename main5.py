import mysql.connector
import random


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


for subject in subjects:
    if subject['subject_name'] == "CHEM F110":
        CHEMF110_slots.append(subject)
    elif subject['subject_name'] == "CHEM F111":
        CHEMF111_slots.append(subject)
    elif subject['subject_name'] == "EEE F111":
        EEEF111_slots.append(subject)
    elif subject['subject_name'] == "ME F112":
        MEF112_slots.append(subject)
    elif subject['subject_name'] == "PHY F111":
        PHYF111_slots.append(subject)
    elif subject['subject_name'] == "MATH F111":
        MATHF111_slots.append(subject)
    elif subject['subject_name'] == "PHY TF111":
        PHYTF111_slots.append(subject)
    elif subject['subject_name'] == "MATH TF111":
        MATHTF111_slots.append(subject)
    elif subject['subject_name'] == "EEE TF111":
        EEETF111_slots.append(subject)
    elif subject['subject_name'] == "CHEM TF111":
        CHEMTF111_slots.append(subject)
    elif subject['subject_name'] == "ME F112 LEC":
        MEF112L_slots.append(subject)
    elif subject['subject_name'] == "PHY F110":
        PHYF110_slots.append(subject)


subject_list = {
    'CHEM_F111': CHEMF111_slots,
    'CHEM_F110': CHEMF110_slots,
    'EEE_F111': EEEF111_slots,
    'ME_F112': MEF112_slots,
    'PHY_F111': PHYF111_slots,
    'MATH_F111': MATHF111_slots,
    'PHY_TF111': PHYTF111_slots,
    'MATH_TF111': MATHTF111_slots,
    'EEE_TF111': EEETF111_slots,
    'CHEM_TF111': CHEMTF111_slots,
    'ME_F112L': MEF112L_slots,
    'PHY_F110': PHYF110_slots,
}


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
