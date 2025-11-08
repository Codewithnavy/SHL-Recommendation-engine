from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.models import QueryRequest, RecommendationResponse, HealthResponse, AssessmentResponse
from app.recommender import AssessmentRecommender
from app.config import settings
import os

app = FastAPI(
    title="SHL Assessment Recommendation API",
    description="Intelligent recommendation system for SHL assessments",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize recommender
recommender = AssessmentRecommender()

@app.get("/", response_class=FileResponse)
async def root():
    """Serve the frontend HTML."""
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"message": "SHL Assessment Recommendation API is running"}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return HealthResponse(status="healthy")

@app.post("/recommend", response_model=RecommendationResponse)
async def recommend(request: QueryRequest):
    """
    Recommendation endpoint that accepts a job description or natural language query
    and returns recommended relevant assessments.
    
    Request:
    - query: Natural language query or job description text
    
    Response:
    - recommended_assessments: List of at least 5, at most 10 relevant assessments
    """
    try:
        if not request.query or len(request.query.strip()) < 10:
            raise HTTPException(
                status_code=400, 
                detail="Query must be at least 10 characters long"
            )
        
        # Get recommendations
        recommendations = recommender.get_recommendations(
            request.query, 
            top_k=settings.MAX_RECOMMENDATIONS
        )
        
        # Ensure we have at least minimum recommendations
        if len(recommendations) < settings.MIN_RECOMMENDATIONS:
            # Pad with top assessments if needed
            all_assessments = recommender.assessments[:settings.MIN_RECOMMENDATIONS]
            recommendations.extend([a for a in all_assessments if a not in recommendations])
        
        # Format response
        formatted_recommendations = recommender.format_response(
            recommendations[:settings.MAX_RECOMMENDATIONS]
        )
        
        # Convert to response models
        assessment_responses = [
            AssessmentResponse(**rec) for rec in formatted_recommendations
        ]
        
        return RecommendationResponse(recommended_assessments=assessment_responses)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/assessments/count")
async def get_assessment_count():
    """Get the total number of assessments in the database."""
    return {"count": len(recommender.assessments)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
