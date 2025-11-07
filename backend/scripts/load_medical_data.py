
import json
import os
import sys
from pathlib import Path
from typing import List, Dict
import logging

sys.path.append(str(Path(__file__).parent.parent))

from app.rag.vectorstore import get_vector_store

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MedicalDataLoader:
    
    def __init__(self):
        self.vector_store = get_vector_store()
        self.data_dir = Path(__file__).parent.parent / "data" / "medical_knowledge"
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def load_icd10_codes(self) -> List[Dict]:
        logger.info("Loading ICD-10 disease codes...")
        
        icd10_data = [
            {
                "code": "A00-B99",
                "category": "Infectious Diseases",
                "text": "Infectious and parasitic diseases include bacterial infections, viral diseases, fungal infections, and parasitic diseases. Common symptoms include fever, fatigue, body aches, and inflammation. Treatment typically involves antibiotics, antivirals, or antiparasitics depending on the causative agent."
            },
            {
                "code": "I00-I99",
                "category": "Cardiovascular Diseases",
                "text": "Cardiovascular diseases affect the heart and blood vessels. Common conditions include hypertension, coronary artery disease, heart failure, arrhythmias, and stroke. Symptoms may include chest pain, shortness of breath, palpitations, dizziness, and fatigue. Risk factors include smoking, obesity, diabetes, and family history."
            },
            {
                "code": "J00-J99",
                "category": "Respiratory Diseases",
                "text": "Respiratory diseases affect the lungs and airways. Common conditions include asthma, COPD, pneumonia, bronchitis, and influenza. Symptoms include cough, shortness of breath, wheezing, chest tightness, and mucus production. Treatment may include bronchodilators, corticosteroids, antibiotics, and oxygen therapy."
            },
            {
                "code": "K00-K95",
                "category": "Digestive Diseases",
                "text": "Digestive system diseases affect the gastrointestinal tract from mouth to anus. Common conditions include GERD, peptic ulcers, IBS, IBD, hepatitis, and gallstones. Symptoms include abdominal pain, nausea, vomiting, diarrhea, constipation, and bloating. Treatment varies by condition and may include dietary changes, medications, or surgery."
            },
            {
                "code": "M00-M99",
                "category": "Musculoskeletal Diseases",
                "text": "Musculoskeletal diseases affect bones, joints, muscles, and connective tissues. Common conditions include arthritis, osteoporosis, back pain, tendinitis, and fractures. Symptoms include pain, stiffness, swelling, reduced range of motion, and weakness. Treatment may include physical therapy, pain management, anti-inflammatory medications, and surgery."
            },
            {
                "code": "N00-N99",
                "category": "Genitourinary Diseases",
                "text": "Genitourinary diseases affect the kidneys, bladder, and reproductive organs. Common conditions include UTIs, kidney stones, chronic kidney disease, prostate issues, and menstrual disorders. Symptoms vary but may include pain, urinary changes, bleeding, and discharge. Treatment depends on the specific condition."
            },
            {
                "code": "E00-E89",
                "category": "Endocrine Diseases",
                "text": "Endocrine diseases affect hormone-producing glands. Common conditions include diabetes mellitus, thyroid disorders, adrenal disorders, and metabolic syndrome. Symptoms vary widely but may include weight changes, fatigue, mood changes, and metabolic disturbances. Treatment often involves hormone replacement or regulation."
            },
            {
                "code": "F00-F99",
                "category": "Mental Health Disorders",
                "text": "Mental health disorders affect mood, thinking, and behavior. Common conditions include depression, anxiety disorders, bipolar disorder, schizophrenia, and PTSD. Symptoms include mood changes, cognitive difficulties, behavioral changes, and social withdrawal. Treatment includes psychotherapy, medications, and lifestyle modifications."
            },
            {
                "code": "G00-G99",
                "category": "Neurological Diseases",
                "text": "Neurological diseases affect the brain, spinal cord, and nerves. Common conditions include epilepsy, Parkinson's disease, Alzheimer's disease, multiple sclerosis, and migraines. Symptoms include headaches, seizures, tremors, memory loss, weakness, and sensory changes. Treatment varies by condition."
            },
            {
                "code": "L00-L99",
                "category": "Skin Diseases",
                "text": "Dermatological conditions affect the skin, hair, and nails. Common conditions include eczema, psoriasis, acne, dermatitis, fungal infections, and skin cancer. Symptoms include rashes, itching, discoloration, lesions, and texture changes. Treatment may include topical medications, systemic therapy, or procedures."
            }
        ]
        
        return icd10_data
    
    def load_common_medications(self) -> List[Dict]:
        """Load common medication information"""
        logger.info("Loading medication database...")
        
        medications = [
            {
                "name": "Acetaminophen (Tylenol)",
                "category": "Analgesic/Antipyretic",
                "text": "Acetaminophen is used to treat pain and reduce fever. Common uses include headaches, muscle aches, arthritis, backaches, toothaches, colds, and fevers. Dosage: Adults 325-650mg every 4-6 hours, maximum 4000mg/day. Side effects are rare but may include liver damage with overdose. Avoid alcohol while taking."
            },
            {
                "name": "Ibuprofen (Advil, Motrin)",
                "category": "NSAID",
                "text": "Ibuprofen is a nonsteroidal anti-inflammatory drug used for pain, fever, and inflammation. Common uses include headaches, dental pain, menstrual cramps, muscle aches, and arthritis. Dosage: Adults 200-400mg every 4-6 hours, maximum 1200mg/day OTC. Side effects may include stomach upset, heartburn, and increased bleeding risk. Take with food."
            },
            {
                "name": "Amoxicillin",
                "category": "Antibiotic",
                "text": "Amoxicillin is a penicillin antibiotic used to treat bacterial infections including respiratory infections, ear infections, urinary tract infections, and skin infections. Dosage varies by condition. Common side effects include diarrhea, nausea, and rash. Complete full course even if feeling better. Inform doctor of penicillin allergies."
            },
            {
                "name": "Metformin",
                "category": "Antidiabetic",
                "text": "Metformin is used to treat type 2 diabetes by improving insulin sensitivity and reducing glucose production. Dosage typically starts at 500mg twice daily with meals, gradually increased. Common side effects include gastrointestinal upset, diarrhea, and nausea. Take with food to reduce side effects. Regular monitoring of kidney function required."
            },
            {
                "name": "Lisinopril",
                "category": "ACE Inhibitor",
                "text": "Lisinopril is used to treat high blood pressure and heart failure. It works by relaxing blood vessels. Typical dosage 10-40mg once daily. Common side effects include dizziness, headache, persistent dry cough, and fatigue. Monitor blood pressure regularly. Avoid potassium supplements. Can cause birth defects - not for pregnant women."
            },
            {
                "name": "Atorvastatin (Lipitor)",
                "category": "Statin",
                "text": "Atorvastatin is used to lower cholesterol and reduce cardiovascular risk. Typical dosage 10-80mg once daily. Common side effects include muscle pain, digestive problems, and elevated liver enzymes. Avoid grapefruit juice. Regular liver function and lipid monitoring required. Report unexplained muscle pain immediately."
            },
            {
                "name": "Omeprazole (Prilosec)",
                "category": "Proton Pump Inhibitor",
                "text": "Omeprazole reduces stomach acid production, used for GERD, ulcers, and heartburn. Dosage typically 20-40mg once daily before meals. Common side effects include headache, nausea, and diarrhea. Long-term use may affect nutrient absorption. Take 30-60 minutes before first meal of the day."
            },
            {
                "name": "Albuterol",
                "category": "Bronchodilator",
                "text": "Albuterol is a rescue inhaler for asthma and COPD, providing quick relief of breathing difficulties. Dosage: 1-2 puffs every 4-6 hours as needed. Common side effects include tremor, nervousness, rapid heartbeat, and headache. Rinse mouth after use. Seek emergency care if no improvement or using more than prescribed."
            },
            {
                "name": "Sertraline (Zoloft)",
                "category": "SSRI Antidepressant",
                "text": "Sertraline treats depression, anxiety, OCD, PTSD, and panic disorder. Typical dosage 50-200mg once daily. May take 4-6 weeks for full effect. Common side effects include nausea, diarrhea, insomnia, sexual dysfunction, and drowsiness. Do not stop abruptly. Inform doctor of suicidal thoughts."
            },
            {
                "name": "Levothyroxine (Synthroid)",
                "category": "Thyroid Hormone",
                "text": "Levothyroxine treats hypothyroidism by replacing thyroid hormone. Dosage individualized based on lab results, typically 25-200mcg daily. Take on empty stomach 30-60 minutes before breakfast. Common side effects with incorrect dose include palpitations, weight changes, and fatigue. Regular thyroid function monitoring required."
            }
        ]
        
        return medications
    
    def load_symptom_disease_mapping(self) -> List[Dict]:
        """Load symptom-to-disease mappings"""
        logger.info("Loading symptom-disease mappings...")
        
        mappings = [
            {
                "symptoms": "fever, cough, fatigue, body aches",
                "diseases": "Influenza, COVID-19, Common Cold, Pneumonia",
                "text": "Fever with cough and body aches commonly indicates respiratory infections. Influenza presents with sudden onset high fever, dry cough, severe body aches, and fatigue. COVID-19 may include loss of taste/smell. Common cold typically has milder symptoms. Pneumonia may cause chest pain and difficulty breathing. Seek immediate care for severe shortness of breath, chest pain, or high persistent fever."
            },
            {
                "symptoms": "chest pain, shortness of breath, sweating",
                "diseases": "Heart Attack, Angina, Pulmonary Embolism, Panic Attack",
                "text": "Chest pain with shortness of breath requires immediate evaluation. Heart attack (myocardial infarction) presents with crushing chest pain, radiating to arm/jaw, sweating, and nausea. Angina is similar but resolves with rest. Pulmonary embolism causes sudden sharp chest pain and difficulty breathing. Panic attacks can mimic cardiac symptoms. CALL 911 IMMEDIATELY for suspected heart attack."
            },
            {
                "symptoms": "severe headache, stiff neck, fever, confusion",
                "diseases": "Meningitis, Encephalitis, Subarachnoid Hemorrhage",
                "text": "Severe headache with stiff neck and fever suggests meningitis - inflammation of brain/spinal cord membranes. Bacterial meningitis is a medical emergency requiring immediate antibiotics. Symptoms include severe headache, neck stiffness, fever, photophobia, and altered mental status. Viral meningitis is less severe. Subarachnoid hemorrhage causes sudden 'thunderclap' headache. SEEK EMERGENCY CARE IMMEDIATELY."
            },
            {
                "symptoms": "abdominal pain, nausea, vomiting, fever",
                "diseases": "Appendicitis, Gastroenteritis, Cholecystitis, Pancreatitis",
                "text": "Abdominal pain with fever and vomiting has multiple causes. Appendicitis typically starts with periumbilical pain migrating to right lower quadrant, with fever and loss of appetite - requires surgery. Gastroenteritis (stomach flu) causes diffuse cramping with diarrhea. Cholecystitis (gallbladder inflammation) causes right upper quadrant pain after fatty meals. Pancreatitis causes severe upper abdominal pain radiating to back."
            },
            {
                "symptoms": "frequent urination, increased thirst, unexplained weight loss",
                "diseases": "Diabetes Mellitus, Diabetes Insipidus, Hyperthyroidism",
                "text": "Classic triad of increased urination, thirst, and weight loss suggests diabetes mellitus. Type 1 diabetes has rapid onset, typically in younger patients. Type 2 diabetes develops gradually, often in overweight adults. Additional symptoms include blurred vision, slow wound healing, and fatigue. Diabetes insipidus causes excessive urination without elevated blood sugar. Hyperthyroidism causes weight loss with increased appetite."
            },
            {
                "symptoms": "joint pain, stiffness, swelling",
                "diseases": "Rheumatoid Arthritis, Osteoarthritis, Gout, Lupus",
                "text": "Joint pain and stiffness have multiple causes. Rheumatoid arthritis causes symmetric joint pain, morning stiffness >30 minutes, and swelling - an autoimmune condition. Osteoarthritis causes pain worsening with activity, typically in weight-bearing joints. Gout causes sudden severe pain, redness, and swelling, often in big toe. Lupus causes joint pain with systemic symptoms like rash and fatigue."
            },
            {
                "symptoms": "persistent cough, weight loss, night sweats, fatigue",
                "diseases": "Tuberculosis, Lung Cancer, Lymphoma, HIV/AIDS",
                "text": "Persistent cough with weight loss and night sweats requires thorough evaluation. Tuberculosis presents with chronic cough (>3 weeks), hemoptysis, weight loss, fever, and night sweats. Lung cancer may cause persistent cough, chest pain, and hemoptysis. Lymphoma causes painless lymph node swelling, fever, night sweats, and weight loss. HIV/AIDS causes progressive immune dysfunction with opportunistic infections."
            },
            {
                "symptoms": "severe sudden headache, vision changes, weakness on one side",
                "diseases": "Stroke, Transient Ischemic Attack, Brain Tumor, Migraine",
                "text": "Sudden severe headache with neurological symptoms suggests stroke. Use FAST assessment: Face drooping, Arm weakness, Speech difficulty, Time to call 911. Ischemic stroke (blocked artery) and hemorrhagic stroke (bleeding) both require immediate treatment. TIA (mini-stroke) has temporary symptoms but warns of stroke risk. Brain tumors cause progressive symptoms. Migraine with aura can mimic stroke but has typical pattern."
            },
            {
                "symptoms": "difficulty breathing, wheezing, chest tightness",
                "diseases": "Asthma, COPD, Anaphylaxis, Heart Failure",
                "text": "Breathing difficulty requires prompt assessment. Asthma causes episodic wheezing, chest tightness, and shortness of breath, often triggered by allergens or exercise. COPD causes progressive dyspnea with chronic cough. Anaphylaxis is severe allergic reaction with rapid onset - use epinephrine immediately. Heart failure causes dyspnea worsening when lying down, with leg swelling. Seek emergency care for severe breathing difficulty."
            },
            {
                "symptoms": "rash, itching, hives, swelling",
                "diseases": "Allergic Reaction, Eczema, Psoriasis, Contact Dermatitis",
                "text": "Skin reactions have various causes. Allergic reactions range from mild (hives, itching) to severe anaphylaxis (throat swelling, difficulty breathing). Eczema causes itchy, inflamed, dry skin patches. Psoriasis causes thick, scaly plaques, often on elbows and knees. Contact dermatitis occurs after exposure to irritants or allergens. Seek emergency care for facial/throat swelling or difficulty breathing."
            }
        ]
        
        return mappings
    
    def load_emergency_protocols(self) -> List[Dict]:
        """Load emergency medical protocols"""
        logger.info("Loading emergency protocols...")
        
        protocols = [
            {
                "emergency": "Cardiac Arrest",
                "text": "CALL 911 IMMEDIATELY. Begin CPR if trained: 30 chest compressions (2 inches deep, 100-120/min) followed by 2 rescue breaths. Use AED if available. Continue until help arrives. Signs: unresponsive, not breathing normally, no pulse. Time is critical - brain damage begins within 4-6 minutes without oxygen."
            },
            {
                "emergency": "Severe Bleeding",
                "text": "CALL 911 for severe bleeding. Apply direct pressure with clean cloth. Do not remove cloth if soaked - add more on top. Elevate injured area above heart if possible. Apply pressure to pressure points if direct pressure insufficient. Use tourniquet only as last resort for life-threatening limb bleeding. Monitor for shock (pale, cold, rapid pulse)."
            },
            {
                "emergency": "Choking",
                "text": "If person can cough/speak, encourage coughing. If cannot breathe/speak: perform Heimlich maneuver - stand behind, wrap arms around waist, make fist above navel, grasp with other hand, give quick upward thrusts. For unconscious person, begin CPR. For infants, use back blows and chest thrusts. CALL 911 if obstruction not cleared."
            },
            {
                "emergency": "Severe Allergic Reaction (Anaphylaxis)",
                "text": "CALL 911 IMMEDIATELY. Use epinephrine auto-injector (EpiPen) in outer thigh if available. Lay person flat, elevate legs. Give second dose after 5-15 minutes if no improvement. Signs: difficulty breathing, throat swelling, rapid pulse, dizziness, hives, nausea. Even if symptoms improve, emergency evaluation required as symptoms can return."
            },
            {
                "emergency": "Stroke",
                "text": "CALL 911 IMMEDIATELY - time is brain. Use FAST test: Face drooping (smile), Arm weakness (raise both arms), Speech difficulty (repeat phrase), Time (note symptom onset time). Do not give food, drink, or medication. Keep person calm and lying down with head slightly elevated. Treatment most effective within 3-4.5 hours of symptom onset."
            },
            {
                "emergency": "Seizure",
                "text": "CALL 911 if: first seizure, lasts >5 minutes, multiple seizures, injury occurs, person has diabetes/pregnancy, or doesn't regain consciousness. During seizure: protect from injury, cushion head, turn on side, loosen tight clothing, time the seizure. DO NOT restrain, put anything in mouth, or give food/drink until fully conscious."
            },
            {
                "emergency": "Severe Burns",
                "text": "CALL 911 for large burns, burns on face/hands/feet/genitals, or third-degree burns. Remove from heat source. Remove jewelry/tight clothing before swelling. Cool burn with cool (not ice) water for 10-20 minutes. Cover with sterile, non-stick bandage. Do not apply ice, butter, or ointments. Treat for shock if needed. Do not break blisters."
            },
            {
                "emergency": "Poisoning",
                "text": "CALL POISON CONTROL (1-800-222-1222) or 911 immediately. Have poison container available. Do not induce vomiting unless instructed. If person unconscious, having seizures, or difficulty breathing, call 911 first. For skin contact, remove contaminated clothing and rinse with water for 15-20 minutes. For eye exposure, flush with water for 15 minutes."
            },
            {
                "emergency": "Diabetic Emergency",
                "text": "Low blood sugar (hypoglycemia): If conscious, give 15g fast-acting carbs (juice, glucose tablets, candy). Recheck in 15 minutes. If unconscious, CALL 911, place in recovery position. High blood sugar (hyperglycemia): Symptoms develop slowly - increased thirst, urination, fatigue. Seek medical care. Diabetic ketoacidosis is emergency: fruity breath, rapid breathing, confusion - CALL 911."
            },
            {
                "emergency": "Head Injury",
                "text": "CALL 911 if: loss of consciousness, severe headache, vomiting, confusion, seizure, clear fluid from nose/ears, unequal pupils, or weakness. Keep person still, stabilize head/neck. Apply ice to swelling. Monitor for deterioration. Do not move if neck injury suspected. Watch for concussion signs: confusion, memory loss, dizziness, nausea. Seek medical evaluation for any significant head trauma."
            }
        ]
        
        return protocols
    
    def load_all_data(self):
        """Load all medical datasets into vector store"""
        logger.info("Starting comprehensive medical data loading...")
        
        all_documents = []
        all_metadatas = []
        all_ids = []
        
        # Load ICD-10 codes
        icd10_data = self.load_icd10_codes()
        for idx, item in enumerate(icd10_data):
            all_documents.append(item['text'])
            all_metadatas.append({
                'source': 'icd10',
                'category': item['category'],
                'code': item['code']
            })
            all_ids.append(f"icd10_{idx}")
        
        # Load medications
        medications = self.load_common_medications()
        for idx, item in enumerate(medications):
            all_documents.append(item['text'])
            all_metadatas.append({
                'source': 'medication',
                'category': item['category'],
                'name': item['name']
            })
            all_ids.append(f"med_{idx}")
        
        # Load symptom mappings
        mappings = self.load_symptom_disease_mapping()
        for idx, item in enumerate(mappings):
            all_documents.append(item['text'])
            all_metadatas.append({
                'source': 'symptom_mapping',
                'symptoms': item['symptoms'],
                'diseases': item['diseases']
            })
            all_ids.append(f"symptom_{idx}")
        
        # Load emergency protocols
        protocols = self.load_emergency_protocols()
        for idx, item in enumerate(protocols):
            all_documents.append(item['text'])
            all_metadatas.append({
                'source': 'emergency_protocol',
                'emergency': item['emergency']
            })
            all_ids.append(f"emergency_{idx}")
        
        # Add all documents to vector store
        logger.info(f"Adding {len(all_documents)} documents to vector store...")
        self.vector_store.add_documents(
            texts=all_documents,
            metadatas=all_metadatas,
            ids=all_ids
        )
        
        logger.info("✅ Medical data loading complete!")
        logger.info(f"Total documents in vector store: {self.vector_store.get_document_count()}")
        
        # Print summary
        print("\n" + "="*60)
        print("📊 MEDICAL KNOWLEDGE BASE SUMMARY")
        print("="*60)
        print(f"✅ ICD-10 Disease Classifications: {len(icd10_data)}")
        print(f"✅ Common Medications: {len(medications)}")
        print(f"✅ Symptom-Disease Mappings: {len(mappings)}")
        print(f"✅ Emergency Protocols: {len(protocols)}")
        print(f"📦 Total Documents: {len(all_documents)}")
        print("="*60)


def main():
    """Main execution"""
    print("🏥 Dr.Heal AI - Medical Data Loader")
    print("="*60)
    
    loader = MedicalDataLoader()
    
    loader.load_all_data()
    
    print("\n✅ Medical knowledge base is ready!")
    print("🚀 Your agents now have access to comprehensive medical knowledge!")


if __name__ == "__main__":
    main()
