from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List

from database import (
    clear_analysis_history,
    database_is_healthy,
    get_analysis_history,
    save_analysis,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for model and tokenizer
tokenizer = None
model = None
device = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage the lifespan of the FastAPI app - startup and shutdown"""
    # Startup
    global tokenizer, model, device

    try:
        # Check if CUDA is available
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"Using device: {device}")

        # Load tokenizer and model
        logger.info("Loading DistilBERT model and tokenizer...")
        tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
        model = DistilBertForSequenceClassification.from_pretrained(
            'distilbert-base-uncased-finetuned-sst-2-english'
        )

        # Move model to GPU if available
        model = model.to(device)
        model.eval()  # Set to evaluation mode

        logger.info("Model loaded successfully!")

    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise e
    
    yield  # App runs here
    
    # Shutdown (cleanup if needed)
    logger.info("Shutting down...")

# Initialize FastAPI app with lifespan
app = FastAPI(
    title="DistilBERT Sentiment Analysis API",
    description="A simple API for sentiment analysis using DistilBERT",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS middleware to allow requests from any origin (useful for development; restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class TextInput(BaseModel):
    text: str

class SentimentResult(BaseModel):
    text: str
    sentiment: str
    confidence: float

class AnalysisHistoryItem(SentimentResult):
    id: int
    created_at: datetime

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "DistilBERT Sentiment Analysis API",
        "endpoints": {
            "/analyze": "POST - Analyze sentiment of text",
            "/health": "GET - Health check",
            "/history": "GET - List recent analyses; DELETE - Clear history"
        },
        "example": {
            "input": {"text": "I love this movie! It's absolutely fantastic."},
            "output": {"text": "I love this movie! It's absolutely fantastic.", "sentiment": "POSITIVE", "confidence": 0.999}
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    if not database_is_healthy():
        raise HTTPException(status_code=503, detail="Database not available")
    return {"status": "healthy", "device": str(device), "database": "connected"}

@app.get("/history", response_model=List[AnalysisHistoryItem])
async def list_analysis_history(limit: int = 10):
    """Return the most recent persisted sentiment analyses."""
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")

    try:
        return get_analysis_history(limit)
    except Exception as error:
        logger.error(f"Error reading analysis history: {str(error)}")
        raise HTTPException(status_code=503, detail="Database not available")

@app.delete("/history")
async def delete_analysis_history():
    """Delete all persisted sentiment analyses."""
    try:
        deleted_count = clear_analysis_history()
        return {"deleted_count": deleted_count}
    except Exception as error:
        logger.error(f"Error clearing analysis history: {str(error)}")
        raise HTTPException(status_code=503, detail="Database not available")

@app.post("/analyze", response_model=SentimentResult)
async def analyze_sentiment(input_data: TextInput):
    """Analyze sentiment of the provided text"""

    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    if not input_data.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        # Tokenize the input text
        inputs = tokenizer(
            input_data.text,
            return_tensors='pt',
            padding=True,
            truncation=True,
            max_length=512  # DistilBERT max sequence length
        )

        # Move inputs to the same device as model
        inputs = {key: value.to(device) for key, value in inputs.items()}

        # Make prediction
        with torch.no_grad():
            outputs = model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

        # Get results
        labels = ['NEGATIVE', 'POSITIVE']
        predicted_class = torch.argmax(predictions, dim=-1).item()
        predicted_label = labels[predicted_class]
        confidence = torch.max(predictions).item()

        rounded_confidence = round(confidence, 3)
        save_analysis(input_data.text, predicted_label, rounded_confidence)

        return SentimentResult(
            text=input_data.text,
            sentiment=predicted_label,
            confidence=rounded_confidence
        )

    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
