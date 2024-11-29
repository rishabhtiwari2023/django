from transformers import pipeline

# Load the pre-trained emotion recognition pipeline
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

# Example text
text = "i am buttom of the world!"

# Predict emotion
result = emotion_classifier(text)
print(result)
