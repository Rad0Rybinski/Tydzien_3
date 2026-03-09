import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field


class CodeReviewResult(BaseModel):
    overall_score: str = Field(
        description="Ocena jakości kodu w skali podanej przez użytkownika."
    )
    found_issues: list[str] = Field(
        description="Lista znalezionych problemów, błędów logicznych lub naruszeń dobrych praktyk."
    )
    improved_code: str = Field(
        description="Kompletny, poprawiony kod źródłowy zawierający zalecone poprawki."
    )

def main():
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    wybrany_jezyk = "Python"
    wybrana_skala = "1-10"
    kod_od_usera = """
    def policz_sume(a, b):
      wynik=a+b
      return wynik
    """

    moj_prompt = f"""
    <instruction>
    You are a senior {wybrany_jezyk} developer conducting a professional code review.

    Review guidelines:
    - Rate the code quality on a scale of {wybrana_skala} (return only the score, e.g. "7/10").
    - Identify issues in the following categories: readability, naming conventions,
      style (PEP 8), missing type hints, missing docstrings, performance, potential bugs.
    - In the improved code, apply type hints, docstrings, and PEP 8 conventions.
    - Write all text fields (found_issues, overall_score description) in Polish.
    </instruction>

    <scale>{wybrana_skala}</scale>
    <code>
    {kod_od_usera}
    </code>
"""


    response = client.responses.parse(
        model="gpt-5-mini",
        input=[{"role": "user", "content": moj_prompt}],
        text_format=CodeReviewResult
    )

    review = response.output_parsed

    print(f"Typ zwróconego obiektu: {type(review)}\n")

    print("=== OCENA ===")
    print(review.overall_score)
    print("\n=== ZNALEZIONE PROBLEMY ===")
    for issue in review.found_issues:
        print(f"- {issue}")
    print("\n=== POPRAWIONY KOD ===")
    print(review.improved_code)

if __name__ == "__main__":
    main()