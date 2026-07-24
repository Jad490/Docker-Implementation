import os

from transformers import AutoModelForSequenceClassification, AutoTokenizer


model_id = os.getenv(
    "MODEL_ID",
    "distilbert-base-uncased-finetuned-sst-2-english",
)
model_path = os.getenv("MODEL_PATH", "/opt/sentiment-model")

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSequenceClassification.from_pretrained(model_id)
tokenizer.save_pretrained(model_path)
model.save_pretrained(model_path)
