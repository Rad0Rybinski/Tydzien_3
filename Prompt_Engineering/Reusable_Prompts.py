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

    response = client.responses.parse(
        prompt={
          "id": "pmpt_69ade94df2e08195a70dc9fd1f06588f0dc1024bae15641f",
          "version": "1",
          "variables": {
              "wybrany_jezyk": wybrany_jezyk,
              "wybrana_skala": wybrana_skala,
              "kod_od_usera": kod_od_usera
            }
        },
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