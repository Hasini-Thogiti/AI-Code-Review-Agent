from google import genai

client = genai.Client(api_key="AIzaSyAH4hM6_MW1-gqm1yerpGtzL5Mxi3_DyaM")

def reflect_review(code, review):

    reflection_prompt = f"""
    Analyze the original code and the AI review.

    ONLY mention important points that were missed.

    Keep response very short.

    Original Code:
    {code}

    AI Review:
    {review}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=reflection_prompt
    )

    return response.text