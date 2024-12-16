import random
import pandas as pd

# Function to load CSV data into lists
def load_data_from_csv(file_path):
    return pd.read_csv(file_path).iloc[:, 0].tolist()

# Function to generate a sentence with a specific intent
def generate_sentence(intent):
    if intent == "add_patient":
        patient = random.choice(patients)
        age = random.randint(20, 80)
        disease = random.choice(diseases)
        return f"add new patient {patient} {age} years old with {disease}"

    elif intent == "assign_medication":
        patient = random.choice(patients)
        medication = random.choice(medications)
        dosage = random.choice(dosages)
        return f"assign medication {medication} {dosage} for {patient}"

    elif intent == "update_medication":
        patient = random.choice(patients)
        medication = random.choice(medications)
        dosage = random.choice(dosages)
        return f"update medication dosage for {medication} to {dosage} for {patient}"

    elif intent == "remove_medication":
        patient = random.choice(patients)
        medication = random.choice(medications)
        return f"remove medication {medication} from {patient}'s treatment plan"

    elif intent == "get_patient_info":
        patient = random.choice(patients)
        return f"get patient information for {patient}"

    elif intent == "schedule_appointment":
        patient = random.choice(patients)
        return f"schedule appointment for {patient} next week"

    elif intent == "add_allergy":
        patient = random.choice(patients)
        allergy = random.choice(allergies)
        return f"add allergy to {allergy} for {patient}"

    elif intent == "check_lab_results":
        patient = random.choice(patients)
        return f"check lab results for {patient}"

    elif intent == "order_blood_test":
        patient = random.choice(patients)
        return f"order blood test for {patient}"

    elif intent == "update_contact_info":
        patient = random.choice(patients)
        return f"update patient contact info for {patient}"

    elif intent == "order_xray":
        patient = random.choice(patients)
        return f"order x-ray for {patient}"

    elif intent == "consult_specialist":
        patient = random.choice(patients)
        specialty = random.choice(["cardiologist", "dermatologist", "neurologist", "gastroenterologist", "orthopedic surgeon"])
        return f"consult with a {specialty} for {patient}"

    elif intent == "update_medical_history":
        patient = random.choice(patients)
        return f"update medical history for {patient}"

    elif intent == "schedule_surgery":
        patient = random.choice(patients)
        surgery = random.choice(["knee surgery", "heart bypass", "appendectomy", "spinal surgery", "cataract surgery"])
        return f"schedule {surgery} for {patient}"

    elif intent == "discharge_patient":
        patient = random.choice(patients)
        return f"discharge patient {patient}"

# Generate a dataset with a mix of intents
def generate_dataset(num_samples=300):
    data = []
    for _ in range(num_samples):
        intent = random.choice(list(intents.keys()))
        sentence = generate_sentence(intent)
        data.append([sentence, intent])

    df = pd.DataFrame(data, columns=["Sentence", "Intent"])
    return df

NUMRECORDS = 300
PATHPREFIX = r"C:\Users\ideapad\Desktop\MedicalTaskManager\ModelFinetune\CSVs\\"
# Load data from CSV files
files_list = ['patients.csv', 'medications.csv', 'dosages.csv', 'diseases.csv', 'allergies.csv', 'actions.csv']
data = []

for file in files_list:
    data.append(load_data_from_csv(PATHPREFIX + file))

patients, medications, dosages, diseases, allergies, actions = data

# Load intents separately for mapping
intents_data = pd.read_csv(PATHPREFIX + 'intents.csv')

# Mapping intents
intents = dict(zip(intents_data['intent_name'], intents_data['intent_description']))

# Generate the dataset and save it to a CSV file
dataset = generate_dataset(NUMRECORDS)
dataset.to_csv("expanded_medical_intent_dataset.csv", index=False)

print(dataset.head())  # Preview the first few rows
