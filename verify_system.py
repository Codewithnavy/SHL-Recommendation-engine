"""
Verification script to test all components of the SHL Assessment Recommendation System
"""

import sys
import os

def test_imports():
    """Test all required imports"""
    print("Testing imports...")
    try:
        import google.generativeai as genai
        print("  ✓ google.generativeai")
    except ImportError as e:
        print(f"  ✗ google.generativeai: {e}")
        return False
    
    try:
        from sklearn.metrics.pairwise import cosine_similarity
        print("  ✓ sklearn")
    except ImportError as e:
        print(f"  ✗ sklearn: {e}")
        return False
    
    try:
        import pandas as pd
        print("  ✓ pandas")
    except ImportError as e:
        print(f"  ✗ pandas: {e}")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("  ✓ beautifulsoup4")
    except ImportError as e:
        print(f"  ✗ beautifulsoup4: {e}")
        return False
    
    try:
        import fastapi
        print("  ✓ fastapi")
    except ImportError as e:
        print(f"  ✗ fastapi: {e}")
        return False
    
    return True

def test_data_files():
    """Test that required data files exist"""
    print("\nTesting data files...")
    required_files = [
        'data/assessments.json',
        'data/train_set.csv',
        'data/test_set.csv',
        'static/index.html',
        'requirements.txt',
        'README.md',
        'APPROACH.md'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - NOT FOUND")
            all_exist = False
    
    return all_exist

def test_modules():
    """Test custom modules can be imported"""
    print("\nTesting custom modules...")
    try:
        from app.recommender import AssessmentRecommender
        print("  ✓ app.recommender")
    except Exception as e:
        print(f"  ✗ app.recommender: {e}")
        return False
    
    try:
        from app.main import app
        print("  ✓ app.main")
    except Exception as e:
        print(f"  ✗ app.main: {e}")
        return False
    
    try:
        from evaluation.evaluate import calculate_recall_at_k
        print("  ✓ evaluation.evaluate")
    except Exception as e:
        print(f"  ✗ evaluation.evaluate: {e}")
        return False
    
    return True

def test_recommender():
    """Test the recommendation engine"""
    print("\nTesting recommendation engine...")
    try:
        from app.recommender import AssessmentRecommender
        recommender = AssessmentRecommender()
        
        num_assessments = len(recommender.assessments)
        print(f"  ✓ Loaded {num_assessments} assessments")
        
        if num_assessments < 10:
            print(f"  ✗ Expected at least 10 assessments, got {num_assessments}")
            return False
        
        # Test keyword-based recommendation (doesn't need API key)
        test_query = "I need Java developers who can collaborate with teams"
        recommendations = recommender.keyword_based_recommendations(test_query, 5)
        
        if len(recommendations) > 0:
            print(f"  ✓ Generated {len(recommendations)} recommendations (keyword-based)")
            print(f"    First recommendation: {recommendations[0]['name']}")
        else:
            print("  ✗ No recommendations generated")
            return False
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_evaluation():
    """Test evaluation functions"""
    print("\nTesting evaluation functions...")
    try:
        from evaluation.evaluate import calculate_recall_at_k
        
        # Test recall calculation
        relevant = ['url1', 'url2', 'url3']
        recommended = ['url1', 'url4', 'url2', 'url5', 'url6']
        recall = calculate_recall_at_k(relevant, recommended, 5)
        
        expected = 2/3  # 2 out of 3 relevant items found
        if abs(recall - expected) < 0.01:
            print(f"  ✓ Recall calculation correct: {recall:.4f}")
        else:
            print(f"  ✗ Recall calculation incorrect: {recall:.4f}, expected {expected:.4f}")
            return False
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_integrity():
    """Test data file integrity"""
    print("\nTesting data integrity...")
    try:
        import json
        import pandas as pd
        
        # Test assessments file
        with open('data/assessments.json', 'r', encoding='utf-8') as f:
            assessments = json.load(f)
        
        if len(assessments) > 0:
            print(f"  ✓ assessments.json: {len(assessments)} assessments")
            
            # Check required fields
            required_fields = ['url', 'name', 'description', 'duration', 'test_type']
            first_assessment = assessments[0]
            missing_fields = [f for f in required_fields if f not in first_assessment]
            
            if missing_fields:
                print(f"  ✗ Missing fields in assessments: {missing_fields}")
                return False
            else:
                print(f"  ✓ All required fields present")
        else:
            print("  ✗ assessments.json is empty")
            return False
        
        # Test training data
        train_df = pd.read_csv('data/train_set.csv')
        print(f"  ✓ train_set.csv: {len(train_df)} rows")
        
        # Test test data
        test_df = pd.read_csv('data/test_set.csv')
        print(f"  ✓ test_set.csv: {len(test_df)} rows")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("="*80)
    print("SHL Assessment Recommendation System - Verification")
    print("="*80)
    
    results = []
    
    # Run all tests
    results.append(("Imports", test_imports()))
    results.append(("Data Files", test_data_files()))
    results.append(("Modules", test_modules()))
    results.append(("Data Integrity", test_data_integrity()))
    results.append(("Recommender", test_recommender()))
    results.append(("Evaluation", test_evaluation()))
    
    # Summary
    print("\n" + "="*80)
    print("VERIFICATION SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name:20s}: {status}")
    
    print("="*80)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All verifications passed! System is ready to use.")
        print("\nNext steps:")
        print("1. Set GOOGLE_API_KEY in .env file")
        print("2. Run: python app/main.py")
        print("3. Visit: http://localhost:8000")
        return 0
    else:
        print(f"\n✗ {total - passed} verification(s) failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
