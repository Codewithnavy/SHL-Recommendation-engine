import requests
import json

def test_health():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        print("✓ Health check passed\n")
        return True
    except Exception as e:
        print(f"✗ Health check failed: {e}\n")
        return False

def test_recommendation():
    """Test the recommendation endpoint"""
    print("Testing recommendation endpoint...")
    
    test_queries = [
        "I am hiring for Java developers who can collaborate effectively with my business teams. Looking for assessments that can be completed in 40 minutes.",
        "I want to hire a Senior Data Analyst with 5 years of experience and expertise in SQL, Excel and Python.",
        "Looking to hire mid-level professionals who are proficient in Python, SQL and JavaScript."
    ]
    
    for idx, query in enumerate(test_queries, 1):
        print(f"\nTest Query {idx}: {query[:80]}...")
        try:
            response = requests.post(
                "http://localhost:8000/recommend",
                json={"query": query}
            )
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                recommendations = data.get("recommended_assessments", [])
                print(f"Number of recommendations: {len(recommendations)}")
                
                if recommendations:
                    print(f"\nFirst recommendation:")
                    first = recommendations[0]
                    print(f"  Name: {first.get('name')}")
                    print(f"  URL: {first.get('url')}")
                    print(f"  Duration: {first.get('duration')} minutes")
                    print(f"  Test Types: {', '.join(first.get('test_type', []))}")
                
                # Validate response format
                assert len(recommendations) >= 5, "Should return at least 5 recommendations"
                assert len(recommendations) <= 10, "Should return at most 10 recommendations"
                
                for rec in recommendations:
                    assert "url" in rec
                    assert "name" in rec
                    assert "duration" in rec
                    assert "test_type" in rec
                    assert isinstance(rec["test_type"], list)
                
                print("✓ Test passed")
            else:
                print(f"✗ Test failed with status code: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"✗ Test failed: {e}")
    
    return True

def test_assessment_count():
    """Test the assessment count endpoint"""
    print("\nTesting assessment count endpoint...")
    try:
        response = requests.get("http://localhost:8000/assessments/count")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Total assessments: {data.get('count')}")
        assert data.get('count', 0) > 0, "Should have assessments loaded"
        print("✓ Assessment count test passed\n")
        return True
    except Exception as e:
        print(f"✗ Assessment count test failed: {e}\n")
        return False

def main():
    print("="*80)
    print("SHL Assessment Recommendation System - API Tests")
    print("="*80)
    print("\nMake sure the server is running on http://localhost:8000\n")
    
    # Run tests
    results = []
    results.append(("Health Check", test_health()))
    results.append(("Assessment Count", test_assessment_count()))
    results.append(("Recommendations", test_recommendation()))
    
    # Summary
    print("\n" + "="*80)
    print("Test Summary")
    print("="*80)
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    print("\n" + ("All tests passed!" if all_passed else "Some tests failed!"))
    print("="*80)

if __name__ == "__main__":
    main()
