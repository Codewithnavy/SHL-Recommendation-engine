import pandas as pd
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.recommender import AssessmentRecommender
from app.config import settings

def calculate_recall_at_k(relevant_urls, recommended_urls, k=10):
    """
    Calculate Recall@K for a single query.
    
    Recall@K = Number of relevant assessments in top K / Total relevant assessments
    """
    if not relevant_urls:
        return 0.0
    
    recommended_set = set(recommended_urls[:k])
    relevant_set = set(relevant_urls)
    
    hits = len(recommended_set & relevant_set)
    total_relevant = len(relevant_set)
    
    recall = hits / total_relevant if total_relevant > 0 else 0.0
    return recall

def calculate_mean_recall_at_k(results, k=10):
    """
    Calculate Mean Recall@K across all queries.
    """
    recalls = []
    
    for query, data in results.items():
        recall = calculate_recall_at_k(
            data['relevant_urls'],
            data['recommended_urls'],
            k
        )
        recalls.append(recall)
    
    mean_recall = sum(recalls) / len(recalls) if recalls else 0.0
    return mean_recall, recalls

def evaluate_on_train_set():
    """
    Evaluate the recommendation system on the training set.
    """
    print("Loading training data...")
    train_df = pd.read_csv(settings.TRAIN_FILE)
    
    # Group by query to get relevant assessments
    query_groups = train_df.groupby('Query')['Assessment_url'].apply(list).to_dict()
    
    print(f"Loaded {len(query_groups)} unique queries")
    
    # Initialize recommender
    print("Initializing recommender...")
    recommender = AssessmentRecommender()
    
    # Evaluate each query
    results = {}
    
    for idx, (query, relevant_urls) in enumerate(query_groups.items(), 1):
        print(f"\nEvaluating query {idx}/{len(query_groups)}")
        print(f"Query: {query[:100]}...")
        
        # Get recommendations
        recommendations = recommender.get_recommendations(query, top_k=10)
        recommended_urls = [rec['url'] for rec in recommendations]
        
        # Calculate recall
        recall = calculate_recall_at_k(relevant_urls, recommended_urls, k=10)
        
        print(f"Relevant: {len(relevant_urls)}, Recommended: {len(recommended_urls)}")
        print(f"Recall@10: {recall:.4f}")
        
        results[query] = {
            'relevant_urls': relevant_urls,
            'recommended_urls': recommended_urls,
            'recall': recall
        }
    
    # Calculate mean recall
    mean_recall, recalls = calculate_mean_recall_at_k(results, k=10)
    
    print("\n" + "="*80)
    print("EVALUATION RESULTS")
    print("="*80)
    print(f"Mean Recall@10: {mean_recall:.4f}")
    print(f"Min Recall@10: {min(recalls):.4f}")
    print(f"Max Recall@10: {max(recalls):.4f}")
    print("="*80)
    
    # Save detailed results
    results_file = os.path.join('evaluation', 'train_evaluation_results.json')
    os.makedirs('evaluation', exist_ok=True)
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            'mean_recall_at_10': mean_recall,
            'min_recall': min(recalls),
            'max_recall': max(recalls),
            'per_query_results': {
                query: {
                    'recall': data['recall'],
                    'num_relevant': len(data['relevant_urls']),
                    'num_recommended': len(data['recommended_urls'])
                }
                for query, data in results.items()
            }
        }, f, indent=2)
    
    print(f"\nDetailed results saved to {results_file}")
    
    return mean_recall

if __name__ == "__main__":
    evaluate_on_train_set()
