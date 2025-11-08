import json
import os
from typing import List, Dict
import google.generativeai as genai
from app.config import settings
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class AssessmentRecommender:
    def __init__(self):
        self.assessments = []
        self.embeddings = []
        self.load_assessments()
        
        # Configure Gemini API
        if settings.GOOGLE_API_KEY:
            genai.configure(api_key=settings.GOOGLE_API_KEY)
        
    def load_assessments(self):
        """Load assessments from JSON file."""
        if os.path.exists(settings.ASSESSMENTS_FILE):
            with open(settings.ASSESSMENTS_FILE, 'r', encoding='utf-8') as f:
                self.assessments = json.load(f)
            print(f"Loaded {len(self.assessments)} assessments")
        else:
            print("No assessments file found. Please run scraper first.")
            
    def get_embedding(self, text: str) -> List[float]:
        """
        Get embedding for text using Gemini API.
        """
        try:
            result = genai.embed_content(
                model=settings.EMBEDDING_MODEL,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"Error getting embedding: {e}")
            # Fallback to simple word-based similarity if API fails
            return None
    
    def create_assessment_text(self, assessment: Dict) -> str:
        """
        Create searchable text from assessment data.
        """
        text_parts = [
            assessment.get('name', ''),
            assessment.get('description', ''),
            ' '.join(assessment.get('test_type', [])),
        ]
        return ' '.join(text_parts)
    
    def get_recommendations(self, query: str, top_k: int = 10) -> List[Dict]:
        """
        Get top K recommendations for a query.
        Implements balanced recommendations across test types.
        """
        if not self.assessments:
            return []
        
        try:
            # Get query embedding
            query_embedding = self.get_embedding(query)
            
            if query_embedding is None:
                # Fallback to keyword-based matching
                return self.keyword_based_recommendations(query, top_k)
            
            # Get embeddings for all assessments if not cached
            if not self.embeddings:
                print("Generating embeddings for assessments...")
                for assessment in self.assessments:
                    text = self.create_assessment_text(assessment)
                    emb = self.get_embedding(text)
                    self.embeddings.append(emb if emb else [0] * 768)
            
            # Calculate similarity scores
            query_emb = np.array(query_embedding).reshape(1, -1)
            assessment_embs = np.array(self.embeddings)
            similarities = cosine_similarity(query_emb, assessment_embs)[0]
            
            # Get top candidates
            top_indices = np.argsort(similarities)[::-1][:top_k * 2]
            
            # Balance recommendations across test types
            recommendations = self.balance_recommendations(top_indices, similarities, query, top_k)
            
            return recommendations[:top_k]
            
        except Exception as e:
            print(f"Error in get_recommendations: {e}")
            return self.keyword_based_recommendations(query, top_k)
    
    def balance_recommendations(self, indices: List[int], similarities: np.ndarray, 
                                query: str, top_k: int) -> List[Dict]:
        """
        Balance recommendations across different test types.
        E.g., if query mentions both technical and behavioral aspects,
        include both types in results.
        """
        query_lower = query.lower()
        
        # Detect query intent
        has_technical = any(kw in query_lower for kw in 
                           ['java', 'python', 'programming', 'technical', 'coding', 'sql', 
                            'developer', 'software', 'engineer'])
        has_behavioral = any(kw in query_lower for kw in 
                            ['collaborate', 'communication', 'personality', 'behavioral', 
                             'leadership', 'team', 'cultural'])
        has_cognitive = any(kw in query_lower for kw in 
                           ['cognitive', 'reasoning', 'aptitude', 'numerical', 'verbal'])
        has_sales = any(kw in query_lower for kw in ['sales', 'customer', 'marketing'])
        
        # Categorize candidates
        technical_recs = []
        behavioral_recs = []
        cognitive_recs = []
        sales_recs = []
        other_recs = []
        
        for idx in indices:
            assessment = self.assessments[idx].copy()
            assessment['_score'] = float(similarities[idx])
            
            test_types = ' '.join(assessment.get('test_type', [])).lower()
            
            if 'knowledge' in test_types or 'skills' in test_types:
                technical_recs.append(assessment)
            elif 'personality' in test_types or 'behavior' in test_types:
                behavioral_recs.append(assessment)
            elif 'ability' in test_types or 'aptitude' in test_types:
                cognitive_recs.append(assessment)
            elif 'competencies' in test_types:
                if 'sales' in assessment.get('name', '').lower():
                    sales_recs.append(assessment)
                else:
                    other_recs.append(assessment)
            else:
                other_recs.append(assessment)
        
        # Build balanced result
        balanced_results = []
        
        if has_technical and has_behavioral:
            # Mix technical and behavioral
            target_technical = top_k // 2
            target_behavioral = top_k - target_technical
            balanced_results.extend(technical_recs[:target_technical])
            balanced_results.extend(behavioral_recs[:target_behavioral])
        elif has_technical:
            # Mostly technical with some cognitive
            balanced_results.extend(technical_recs[:top_k - 2])
            balanced_results.extend(cognitive_recs[:2])
        elif has_behavioral:
            # Mostly behavioral
            balanced_results.extend(behavioral_recs[:top_k - 2])
            balanced_results.extend(cognitive_recs[:2])
        elif has_sales:
            # Sales focused
            balanced_results.extend(sales_recs[:top_k - 2])
            balanced_results.extend(behavioral_recs[:2])
        else:
            # General mix
            balanced_results.extend(technical_recs[:3])
            balanced_results.extend(behavioral_recs[:3])
            balanced_results.extend(cognitive_recs[:2])
            balanced_results.extend(other_recs[:2])
        
        # Fill remaining slots with highest scoring
        if len(balanced_results) < top_k:
            remaining = [self.assessments[i].copy() for i in indices 
                        if self.assessments[i] not in balanced_results]
            balanced_results.extend(remaining[:top_k - len(balanced_results)])
        
        # Remove duplicates while preserving order
        seen_urls = set()
        unique_results = []
        for rec in balanced_results:
            if rec['url'] not in seen_urls:
                seen_urls.add(rec['url'])
                unique_results.append(rec)
        
        return unique_results
    
    def keyword_based_recommendations(self, query: str, top_k: int) -> List[Dict]:
        """
        Fallback keyword-based recommendation when embeddings fail.
        """
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        scored_assessments = []
        
        for assessment in self.assessments:
            text = self.create_assessment_text(assessment).lower()
            text_words = set(text.split())
            
            # Simple word overlap score
            overlap = len(query_words & text_words)
            
            # Boost score for key matches
            if any(word in text for word in ['java', 'python', 'sql'] if word in query_lower):
                overlap += 5
            
            if overlap > 0:
                assessment_copy = assessment.copy()
                assessment_copy['_score'] = overlap
                scored_assessments.append(assessment_copy)
        
        # Sort by score
        scored_assessments.sort(key=lambda x: x['_score'], reverse=True)
        
        return scored_assessments[:top_k]
    
    def format_response(self, recommendations: List[Dict]) -> List[Dict]:
        """
        Format recommendations according to API specification.
        """
        formatted = []
        for rec in recommendations:
            formatted.append({
                "url": rec.get('url', ''),
                "name": rec.get('name', ''),
                "adaptive_support": rec.get('adaptive_support', 'No'),
                "description": rec.get('description', ''),
                "duration": rec.get('duration', 60),
                "remote_support": rec.get('remote_support', 'Yes'),
                "test_type": rec.get('test_type', [])
            })
        return formatted
