from gigachat import GigaChat


TOKEN = ""

def connect_gigachat():
    model = GigaChat(
        credentials=TOKEN,
        model="GigaChat-Pro",
        verify_ssl_certs=False)

    return model

def ask_gigachat(model, prompt):
    response = model.chat({
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "temperature": 0.1,
        "top_p": 0.9,

    })
    return response.choices[0].message.content


