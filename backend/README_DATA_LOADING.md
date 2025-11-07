# 📊 Medical Data Loading Guide

## Overview

This guide explains how to load comprehensive medical datasets into Dr.Heal AI's RAG system to supercharge agent accuracy.

## What's Included

### 1. **ICD-10 Disease Classifications** (10 categories)
- Infectious Diseases
- Cardiovascular Diseases
- Respiratory Diseases
- Digestive Diseases
- Musculoskeletal Diseases
- Genitourinary Diseases
- Endocrine Diseases
- Mental Health Disorders
- Neurological Diseases
- Skin Diseases

### 2. **Common Medications** (10 drugs)
- Acetaminophen (pain/fever)
- Ibuprofen (NSAID)
- Amoxicillin (antibiotic)
- Metformin (diabetes)
- Lisinopril (blood pressure)
- Atorvastatin (cholesterol)
- Omeprazole (acid reflux)
- Albuterol (asthma)
- Sertraline (antidepressant)
- Levothyroxine (thyroid)

### 3. **Symptom-Disease Mappings** (10 mappings)
- Fever + cough → Respiratory infections
- Chest pain → Cardiac emergencies
- Severe headache → Neurological emergencies
- Abdominal pain → GI conditions
- And more...

### 4. **Emergency Protocols** (10 protocols)
- Cardiac Arrest
- Severe Bleeding
- Choking
- Anaphylaxis
- Stroke
- Seizure
- Severe Burns
- Poisoning
- Diabetic Emergency
- Head Injury

## How to Load Data

### Step 1: Navigate to Backend
```bash
cd backend
```

### Step 2: Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 3: Run Data Loader
```bash
python scripts/load_medical_data.py
```

### Expected Output
```
🏥 Dr.Heal AI - Medical Data Loader
============================================================
INFO:__main__:Loading ICD-10 disease codes...
INFO:__main__:Loading medication database...
INFO:__main__:Loading symptom-disease mappings...
INFO:__main__:Loading emergency protocols...
INFO:__main__:Adding 40 documents to vector store...
INFO:__main__:✅ Medical data loading complete!

============================================================
📊 MEDICAL KNOWLEDGE BASE SUMMARY
============================================================
✅ ICD-10 Disease Classifications: 10
✅ Common Medications: 10
✅ Symptom-Disease Mappings: 10
✅ Emergency Protocols: 10
📦 Total Documents: 40
============================================================

✅ Medical knowledge base is ready!
🚀 Your agents now have access to comprehensive medical knowledge!
```

## How It Improves Your Agents

### Before (Without Datasets)
- Generic responses
- Limited medical knowledge
- Relies only on LLM training data
- Less accurate symptom analysis

### After (With Datasets)
- **SymptomAnalyzerAgent**: Better symptom-to-disease mapping
- **DiseaseExpertAgent**: Comprehensive ICD-10 classifications
- **TreatmentAdvisorAgent**: Accurate medication information
- **EmergencyTriageAgent**: Life-saving emergency protocols

## Verify Data Loading

### Check Document Count
```python
from app.rag.vectorstore import get_vector_store

vector_store = get_vector_store()
print(f"Documents in database: {vector_store.get_document_count()}")
```

### Test RAG Search
```python
results = vector_store.search("chest pain symptoms", n_results=3)
print(results['documents'][0])
```

## Expanding the Dataset

To add more medical knowledge:

1. **Edit** `scripts/load_medical_data.py`
2. **Add** new data to the respective methods:
   - `load_icd10_codes()`
   - `load_common_medications()`
   - `load_symptom_disease_mapping()`
   - `load_emergency_protocols()`
3. **Run** the script again

## Production Deployment

The data loader should be run:
- **Once** during initial deployment
- **After** adding new medical knowledge
- **Periodically** to update medication/protocol information

### Railway Deployment
Add to your deployment script:
```bash
python scripts/load_medical_data.py
```

## Notes

- Data is stored in ChromaDB at `./chroma_db`
- Embeddings use `all-MiniLM-L6-v2` model
- Vector search returns top 5 most relevant documents
- All data is embedded and searchable via semantic similarity

## Future Enhancements

Consider adding:
- [ ] Full ICD-10 code database (70,000+ codes)
- [ ] Complete drug interaction database
- [ ] Medical research papers (PubMedQA)
- [ ] Clinical guidelines
- [ ] Lab test reference ranges
- [ ] Vaccine schedules
- [ ] Nutrition databases

---

**Your agents are now supercharged with comprehensive medical knowledge!** 🚀
