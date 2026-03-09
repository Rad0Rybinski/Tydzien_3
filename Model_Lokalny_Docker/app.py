from openai import OpenAI


client = OpenAI(
    base_url='http://host.docker.internal:11434/v1',
    api_key='ollama',
)

historia = []

print("🤖 Chatbot Ollama gotowy! Wpisz 'quit', aby zakończyć.")

while True:
    pytanie = input("Ty: ")
    
    if pytanie.lower() == "quit":
        break
        
    historia.append({"role": "user", "content": pytanie})
    
    try:
        odpowiedz = client.chat.completions.create(
            model="llama3:latest",
            messages=historia
        )
        
        tekst_odpowiedzi = odpowiedz.choices[0].message.content
        print("AI: " + tekst_odpowiedzi)
        
        historia.append({"role": "assistant", "content": tekst_odpowiedzi})
    except Exception as e:
        print(f"❌ Błąd: {e}")