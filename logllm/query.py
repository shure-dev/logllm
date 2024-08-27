import google.generativeai as genai
import os 

genai.configure(api_key=os.environ['API_KEY'])

def query(user_input: str):
    model = genai.GenerativeModel("gemini-1.5-flash")


    system_prompt = """
        # Convert the following query to a W&B API query:
    """.replace("    ","")

    user_prompt = f"""
    # Here is a user's :{user_input}
    """

    response = model.start_chat(
        history=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )
    
    print(response)
    
    