from google import genai

# Configure Gemini client
client = genai.Client(api_key="AIzaSyBbcZi69IyPb6Ib1pcd5zkAzzQvBu1ecaI")

# Take user input
print("Enter your Python code below:")
print("Type END on a new line when finished.\n")

lines = []

while True:
    line = input()

    if line.strip() == "END":
        break

    lines.append(line)

# Combine all lines into one code block
code = "\n".join(lines)

# Prompt
prompt = f"""
You are a professional Python code reviewer.

Review the code briefly and clearly.

Give output ONLY in this format:

Mistakes:
- point

Improvements:
- point

Best Practices:
- point

Keep the answer short and professional.

Python Code:
{code}
"""

# Generate response
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

# Print AI review
print("\n========== AI CODE REVIEW ==========\n")
print(response.text)