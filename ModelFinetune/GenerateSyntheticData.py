import random
import pandas as pd

# Function to load CSV data into lists
def load_data_from_csv(file_path):
    return pd.read_csv(file_path).iloc[:, 0].tolist()

def generate_patient_ner(patient):
    patient_ner = patient.split()[0] + "/B-PATIENT " + " ".join(patient.split()[1:]) + "/I-PATIENT"
    return patient_ner
def generate_disease_ner(disease):
    disease_ner = disease.split()[0] + "/B-DISEASE " + " ".join(disease.split()[1:]) + "/I-DISEASE"
    return disease_ner
def generate_allergy_ner(allergy):
    allergy_ner = allergy.split()[0] + "/B-ALLERGY " + " ".join(allergy.split()[1:]) + "/I-ALLERGY"
    return allergy_ner
def generate_medication_ner(medication):
    medication_ner = medication.split()[0] + "/B-MEDICATION " + " ".join(medication.split()[1:]) + "/I-MEDICATION"
    return medication_ner
def generate_specialty_ner(specialty):
    specialty_ner = specialty.split()[0] + "/B-SPECIALTY " + " ".join(specialty.split()[1:]) + "/I-SPECIALTY"
    return specialty_ner
def generate_surgery_ner(surgery):
    surgery_ner = surgery.split()[0] + "/B-SURGERY " + " ".join(surgery.split()[1:]) + "/I-SURGERY"
    return surgery_ner
def generate_dosage_ner(dosage):
    dosage_ner = dosage.split()[0] + "/B-DOSAGE " + " ".join(dosage.split()[1:]) + "/I-DOSAGE"
    return dosage_ner

# Function to generate a sentence with a specific intent
def generate_sentence(intent):
    if intent == "add_patient":
        patient = random.choice(patients)
        age = random.randint(20, 80)
        disease = random.choice(diseases)
        patient_ner = generate_patient_ner(patient)
        disease_ner = generate_disease_ner(disease)
        ner = f"add/O {patient_ner}/B-PATIENT {age}/B-AGE years/O old/O with/O {disease_ner}/B-DISEASE"
        return f"add new patient {patient} {age} years old with {disease}", ner

    elif intent == "assign_medication":
        patient = random.choice(patients)
        medication = random.choice(medications)
        dosage = random.choice(dosages)
        return f"assign medication {medication} {dosage} for {patient}", f"assign/O medication/O {generate_medication_ner(medication)}{generate_dosage_ner(dosage)} for/O {generate_patient_ner(patient)}" 

    elif intent == "update_medication":
        patient = random.choice(patients)
        medication = random.choice(medications)
        dosage = random.choice(dosages)
        return f"update medication dosage for {medication} to {dosage} for {patient}", f"update/O medication/O dosage/O for/O {generate_medication_ner(medication)} to/O {generate_dosage_ner(dosage)} for/O {generate_patient_ner(patient)}"

    elif intent == "remove_medication":
        patient = random.choice(patients)
        medication = random.choice(medications)
        return f"remove medication {medication} from {patient}'s treatment plan", f"remove/O medication/O {generate_medication_ner(medication)} from/O {generate_patient_ner(patient)} 's/O treatment/O plan/O"

    elif intent == "get_patient_info":
        patient = random.choice(patients)
        return f"get patient information for {patient}", f"get/O patient/O information/O for/O {generate_patient_ner(patient)}"

    elif intent == "schedule_appointment":
        patient = random.choice(patients)
        return f"schedule appointment for {patient} next week", f"schedule/O appointment/O for/O {generate_patient_ner(patient)} next/O week/O"

    elif intent == "add_allergy":
        patient = random.choice(patients)
        allergy = random.choice(allergies)
        return f"add allergy to {allergy} for {patient}", f"add/O allergy/O to/O {generate_allergy_ner(allergy)} for/O {generate_patient_ner(patient)}"

    elif intent == "check_lab_results":
        patient = random.choice(patients)
        return f"check lab results for {patient}", f"check/O lab/O results/O for/O {generate_patient_ner(patient)}"

    elif intent == "order_blood_test":
        patient = random.choice(patients)
        return f"order blood test for {patient}", f"order/O blood/O test/O for/O {generate_patient_ner(patient)}"

    elif intent == "update_contact_info":
        patient = random.choice(patients)
        return f"update patient contact info for {patient}", f"update/O patient/O contact/O info/O for/O {generate_patient_ner(patient)}"

    elif intent == "order_xray":
        patient = random.choice(patients)
        return f"order x-ray for {patient}", f"order/O x-ray/O for/O {generate_patient_ner(patient)}"

    elif intent == "consult_specialist":
        patient = random.choice(patients)
        specialty = random.choice(["cardiologist", "dermatologist", "neurologist", "gastroenterologist", "orthopedic surgeon"])
        return f"consult with a {specialty} for {patient}", f"consult/O with/O a/O {generate_specialty_ner(specialty)} for/O {generate_patient_ner(patient)}"

    elif intent == "update_medical_history":
        patient = random.choice(patients)
        return f"update medical history for {patient}", f"update/O medical/O history/O for/O {generate_patient_ner(patient)}"

    elif intent == "schedule_surgery":
        patient = random.choice(patients)
        surgery = random.choice(["knee surgery", "heart bypass", "appendectomy", "spinal surgery", "cataract surgery"])
        return f"schedule {surgery} for {patient}", f"schedule/O {generate_surgery_ner(surgery)} for/O {generate_patient_ner(patient)}"

    elif intent == "discharge_patient":
        patient = random.choice(patients)
        return f"discharge patient {patient}", f"discharge/O patient/O {generate_patient_ner(patient)}"

# Generate a dataset with a mix of intents
def generate_dataset(num_samples=300):
    data = []
    for _ in range(num_samples):
        intent = random.choice(list(intents.keys()))
        sentence, ner = generate_sentence(intent)
        data.append([sentence, intent, ner])

    df = pd.DataFrame(data, columns=["Sentence", "Intent", "NER"])
    return df

NUMRECORDS = 300
PATHPREFIX = r"C:\Users\ideapad\Desktop\MedicalTaskManager\ModelFinetune\Entities\\"
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
