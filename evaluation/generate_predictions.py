import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.recommender import AssessmentRecommender
from app.config import settings

def generate_predictions():
    """
    Generate predictions for the test set and save to CSV in the required format.
    """
    print("Loading test data...")
    test_df = pd.read_csv(settings.TEST_FILE)
    
    print(f"Loaded {len(test_df)} test queries")
    
    # Initialize recommender
    print("Initializing recommender...")
    recommender = AssessmentRecommender()
    
    # Store predictions
    predictions = []
    
    for idx, row in test_df.iterrows():
        query = row['Query']
        print(f"\nProcessing query {idx + 1}/{len(test_df)}")
        print(f"Query: {query[:100]}...")
        
        # Get recommendations
        recommendations = recommender.get_recommendations(query, top_k=10)
        
        # Add each recommendation as a separate row
        for rec in recommendations:
            predictions.append({
                'Query': query,
                'Assessment_url': rec['url']
            })
        
        print(f"Generated {len(recommendations)} recommendations")
    
    # Create DataFrame and save
    predictions_df = pd.DataFrame(predictions)
    
    output_file = 'predictions.csv'
    predictions_df.to_csv(output_file, index=False)
    
    print(f"\n{'='*80}")
    print(f"Predictions saved to {output_file}")
    print(f"Total rows: {len(predictions_df)}")
    print(f"{'='*80}")
    
    # Show sample
    print("\nSample predictions:")
    print(predictions_df.head(10))
    
    return predictions_df

if __name__ == "__main__":
    generate_predictions()
