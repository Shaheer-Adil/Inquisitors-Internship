from google import genai
import inspect

# Get the signature of generate_content
client = genai.Client(api_key="test")
sig = inspect.signature(client.models.generate_content)
print("generate_content signature:")
print(sig)
