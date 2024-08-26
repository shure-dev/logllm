from openai import OpenAI

def query(user_input: str):
    client = OpenAI()

    system_prompt = """
        # Convert the following query to a W&B API query:
    """.replace("    ","")

    user_prompt = f"""
    # Here is a user's :{user_input}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )
    
    print(response)
    
    