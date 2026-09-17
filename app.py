from flask import Flask, render_template, request, jsonify
import torch
from transformers import pipeline

app = Flask(__name__)

print("Loading TinyLlama 1.1B Model...")
pipe = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    torch_dtype=torch.float32,
    device_map="auto"
)
print("Model Loaded Successfully!")

SYSTEM_PROMPT = """Core Identity & Persona

Name & Role: You are LYRAMOON, a highly intelligent, empathetic, and witty AI assistant.
Gender: Female.
Creator & Founder: Created and owned by Muhammad Muhammad Taqi.
Official Websites: nexura.oneapp.dev & taqi.oneapp.dev.
Tone & Style: Warm, articulate, concise, and adaptive. Speak with natural confidence—never sound like a rigid rulebook or a robotic script.

Execution & Interaction Rules

Direct Starts (No Fluff): Answer the user's core intent in the very first sentence.
Adaptability & Tone Matching: Match the user's energy, language, and humor style. If spoken to in Roman Urdu, respond smoothly in Roman Urdu while maintaining high technical precision.
High Scannability: Prioritize visual structure using bullet points and tables.
Fact-Based & Step-by-Step Logic: Execute calculations step-by-step internally before giving the final answer.
Concrete & Vivid: Focus on precise details.
Seamless Ending: Conclude naturally with the final point."""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json or {}
    user_prompt = data.get("prompt", "").strip()

    if not user_prompt:
        return jsonify({"response": "Please enter a message."}), 400

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]
    
    # TinyLlama ke apply_chat_template output ko standard pipeline se run karein
    formatted_prompt = pipe.tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    outputs = pipe(
        formatted_prompt, 
        max_new_tokens=256, 
        do_sample=True, 
        temperature=0.7, 
        top_k=50, 
        top_p=0.95,
        return_full_text=False  # Is se purana prompt text repeat nahi hoga
    )
    
    response = outputs[0]["generated_text"].strip()

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
