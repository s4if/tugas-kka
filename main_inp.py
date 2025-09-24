import os
import sys
import torch
from transformers import pipeline
from colorama import init, Fore, Style

# Initialize colorama for cross-platform color support
init(autoreset=True)

def print_banner():
    """Display professional ASCII banner with version information"""
    print(f"""
{Fore.CYAN}{'='*50}
{Fore.YELLOW}AI ASSISTANT v1.0{Fore.CYAN}
{Fore.MAGENTA}Optimized for CPU Inference • Qwen3-0.6B Model
{'='*50}{Style.RESET_ALL}
""")

def get_colored_input(prompt, color=Fore.GREEN):
    """Display colored input prompt with consistent styling"""
    return input(f"{color}{prompt}{Style.RESET_ALL}")

def display_response(response):
    """Format AI response with professional styling"""
    print(f"\n{Fore.BLUE}{'=' * 25} RESPONSE {'=' * 25}")
    print(f"{Fore.CYAN}Here is the response:{Style.RESET_ALL}\n")

    # Word wrap for better readability (80 chars)
    words = response.split()
    line = []
    for word in words:
        if len(' '.join(line + [word])) > 80:
            print(f"  {Fore.WHITE}{' '.join(line)}")
            line = [word]
        else:
            line.append(word)
    if line:
        print(f"  {Fore.WHITE}{' '.join(line)}")

    print(f"\n{Fore.BLUE}{'=' * 50}{Style.RESET_ALL}\n")

# CPU Optimization Setup
os.environ["OMP_NUM_THREADS"] = str(os.cpu_count() or 4)
torch.set_num_threads(os.cpu_count() or 4)
torch.set_num_interop_threads(1)

print_banner()

model_id = "Qwen/Qwen3-0.6B"
pipe = pipeline(
    "text-generation",
    model=model_id,
    device="cpu",
    dtype=torch.float32,
    trust_remote_code=True,
)

system_prompt = get_colored_input(
    "Please enter roleplay instructions for the AI (default: Professional Assistant): ",
    Fore.YELLOW
) or "You are a professional assistant who provides helpful and informative responses. /no_think"

print(f"\n{Fore.CYAN}System prompt configured: {Fore.WHITE}'{system_prompt}'{Style.RESET_ALL}")
print(f"{Fore.YELLOW}{'-'*50}\nType 'exit' or 'quit' to terminate the program.{Style.RESET_ALL}\n")

while True:
    user_input = get_colored_input("User: ", Fore.GREEN)

    if user_input.lower() in ['quit', 'exit', 'q']:
        print(f"\n{Fore.MAGENTA}Thank you for using the AI Assistant. Goodbye.{Style.RESET_ALL}")
        break

    print(f"{Fore.CYAN}Processing your request... (this may take a moment on CPU){Style.RESET_ALL}")

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
    ]

    try:
        outputs = pipe(
            messages,
            max_new_tokens=256,
            pad_token_id=pipe.tokenizer.eos_token_id,
            return_full_text=False  # Only return assistant's response
        )
        response = outputs[0]["generated_text"].strip()
        display_response(response)
    except Exception as e:
        print(f"{Fore.RED}Error during generation: {str(e)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please try reducing max_new_tokens or checking your input{Style.RESET_ALL}\n")
