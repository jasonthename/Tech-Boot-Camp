import whisper

model = whisper.load_model("small")
result = model.transcribe("Untitled.m4a", language="English", fp16=False)
print(result["text"])