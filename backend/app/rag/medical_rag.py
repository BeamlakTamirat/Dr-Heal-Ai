import json
import os
from typing import List, Dict, Optional
import logging

from app.rag.vectorstore import get_vector_store
from app.rag.embeddings import get_embedding_model

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MedicalRAG:
    
    def __init__(self, data_dir: str = "./data/medical_knowledge"):
        
        self.data_dir = data_dir
        self.vector_store = get_vector_store()
        self.embedding_model = get_embedding_model()
        
        logger.info(f"Medical RAG initialized with data directory: {data_dir}")
    
    
    def _load_json_file(self, filename: str) -> Dict:
        
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            logger.info(f"Loading {filename}")
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Loaded {len(data)} entries from {filename}")
            return data
            
        except FileNotFoundError:
            logger.error(f"File not found: {filepath}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {filename}: {e}")
            raise
    
    
    def _format_symptom_text(self, symptom_id: str, symptom_data: Dict) -> str:
        
        text_parts = [f"Symptom: {symptom_id}"]
        
        if "description" in symptom_data:
            text_parts.append(f"Description: {symptom_data['description']}")
        
        if "possible_diseases" in symptom_data:
            diseases = ", ".join(symptom_data['possible_diseases'])
            text_parts.append(f"Possible diseases: {diseases}")
        
        if "severity_indicators" in symptom_data:
            severity = symptom_data['severity_indicators']
            text_parts.append(f"Mild: {severity.get('mild', 'N/A')}")
            text_parts.append(f"Moderate: {severity.get('moderate', 'N/A')}")
            text_parts.append(f"Severe: {severity.get('severe', 'N/A')}")
        
        if "emergency_signs" in symptom_data:
            signs = ", ".join(symptom_data['emergency_signs'])
            text_parts.append(f"Emergency signs: {signs}")
        
        if "common_causes" in symptom_data:
            causes = ", ".join(symptom_data['common_causes'])
            text_parts.append(f"Common causes: {causes}")
        
        if "related_symptoms" in symptom_data:
            related = ", ".join(symptom_data['related_symptoms'])
            text_parts.append(f"Related symptoms: {related}")
        
        
        return "\n".join(text_parts)
    
    
    def _format_disease_text(self, disease_id: str, disease_data: Dict) -> str:
        
        text_parts = [f"Disease: {disease_data.get('name', disease_id)}"]
        
        if "description" in disease_data:
            text_parts.append(f"Description: {disease_data['description']}")
        
        if "common_symptoms" in disease_data:
            symptoms = ", ".join(disease_data['common_symptoms'])
            text_parts.append(f"Common symptoms: {symptoms}")
        
        if "causes" in disease_data:
            causes = ", ".join(disease_data['causes'])
            text_parts.append(f"Causes: {causes}")
        
        if "risk_factors" in disease_data:
            risks = ", ".join(disease_data['risk_factors'])
            text_parts.append(f"Risk factors: {risks}")
        
        if "diagnosis_methods" in disease_data:
            diagnosis = ", ".join(disease_data['diagnosis_methods'])
            text_parts.append(f"Diagnosis methods: {diagnosis}")
        
        if "treatment_options" in disease_data:
            treatments = ", ".join(disease_data['treatment_options'])
            text_parts.append(f"Treatment options: {treatments}")
        
        if "prevention" in disease_data:
            prevention = ", ".join(disease_data['prevention'])
            text_parts.append(f"Prevention: {prevention}")
        
        if "when_to_see_doctor" in disease_data:
            text_parts.append(f"When to see doctor: {disease_data['when_to_see_doctor']}")
        
        if "complications" in disease_data:
            complications = ", ".join(disease_data['complications'])
            text_parts.append(f"Possible complications: {complications}")
        
        return "\n".join(text_parts)
    
    
    def load_knowledge(self, reset: bool = False) -> Dict[str, int]:
        
        if reset:
            logger.info("Resetting vector store")
            self.vector_store.reset()
        
        current_count = self.vector_store.get_document_count()
        if current_count > 0 and not reset:
            logger.info(f"Vector store already contains {current_count} documents. Skipping load.")
            logger.info("Use reset=True to reload data.")
            return {"already_loaded": current_count}
        
        texts = []
        metadatas = []
        ids = []
        
        logger.info("Processing symptoms...")
        symptoms = self._load_json_file("symptoms.json")
        
        for symptom_id, symptom_data in symptoms.items():
            
            text = self._format_symptom_text(symptom_id, symptom_data)
            texts.append(text)
            
            
            metadata = {
                "type": "symptom",
                "id": symptom_id,
                "name": symptom_id.replace("_", " ").title()
            }
            metadatas.append(metadata)
            
            
            ids.append(f"symptom_{symptom_id}")
        
        symptom_count = len(symptoms)
        logger.info(f"Processed {symptom_count} symptoms")
        
        
        logger.info("Processing diseases...")
        diseases = self._load_json_file("diseases.json")
        
        for disease_id, disease_data in diseases.items():
            
            text = self._format_disease_text(disease_id, disease_data)
            texts.append(text)
            
            metadata = {
                "type": "disease",
                "id": disease_id,
                "name": disease_data.get("name", disease_id)
            }
            metadatas.append(metadata)
            
            ids.append(f"disease_{disease_id}")
        
        disease_count = len(diseases)
        logger.info(f"Processed {disease_count} diseases")
        
        
        logger.info(f"Adding {len(texts)} documents to vector store...")
        logger.info("This will take 2-3 minutes (generating embeddings)...")
        
        self.vector_store.add_documents(
            texts=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        total_count = self.vector_store.get_document_count()
        logger.info(f"Successfully loaded {total_count} documents into vector store")
        
        return {
            "symptoms": symptom_count,
            "diseases": disease_count,
            "total": total_count
        }
    
    
    def search(
        self,
        query: str,
        n_results: int = 5,
        filter_type: Optional[str] = None
    ) -> List[Dict]:
        
        filter_metadata = None
        if filter_type:
            filter_metadata = {"type": filter_type}
        
        results = self.vector_store.search(
            query=query,
            n_results=n_results,
            filter_metadata=filter_metadata
        )
        
        formatted_results = []
        
        for i in range(len(results['documents'][0])):
            
            distance = results['distances'][0][i]
            similarity = 1 - (distance / 2)
            
            formatted_results.append({
                "text": results['documents'][0][i],
                "metadata": results['metadatas'][0][i],
                "distance": distance,
                "similarity": similarity
            })
        
        return formatted_results
    
    
    def search_symptoms(self, query: str, n_results: int = 5) -> List[Dict]:
        
        return self.search(query, n_results=n_results, filter_type="symptom")
    
    
    def search_diseases(self, query: str, n_results: int = 5) -> List[Dict]:
        
        return self.search(query, n_results=n_results, filter_type="disease")


_medical_rag = None


def get_medical_rag() -> MedicalRAG:
    
    global _medical_rag
    
    if _medical_rag is None:
        logger.info("Creating global MedicalRAG instance")
        _medical_rag = MedicalRAG()
    
    return _medical_rag