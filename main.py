import os
import torch
from transformers import pipeline

# Optimal thread configuration for CPU inference
num_physical_cores = os.cpu_count()  # Logical cores (hyperthreading included)
torch.set_num_threads(num_physical_cores)  # Maximize parallelism
torch.set_num_interop_threads(1)  # Reduce inter-op parallelism overhead

model_id = "Qwen/Qwen3-0.6B"
pipe = pipeline(
    "text-generation",
    model=model_id,
    device="cpu",  # Explicitly use CPU
    dtype=torch.float32,  # Native CPU precision (faster than bfloat16)
    trust_remote_code=True,  # Required for Qwen models
)

messages = [
    {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak! /no_think"},
    {"role": "user", "content": "Jelaskan Padaku tentang Computational Thinking!"},
]

# Generate response
outputs = pipe(
    messages,
    max_new_tokens=256,
    pad_token_id=pipe.tokenizer.eos_token_id,  # Critical for Qwen CPU inference
)

# Beautified output
print("\n" + "="*60)
print("CONVERSATION")
print("="*60)
print(f"System: {messages[0]['content']}")
print(f"User:   {messages[1]['content']}")
print("\nAssistant Response:")
print("-"*60)
print(outputs[0]["generated_text"][-1]["content"])
print("="*60 + "\n")
