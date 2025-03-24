import openai
from django.http import JsonResponse
from django.shortcuts import render

# Replace with your OpenAI API Key
openai.api_key = "key"

def chatbot(request):
    return render(request, "chat.html")

def get_response(request):
    if request.method == "POST":
        user_input = request.POST.get("message")

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            store=True,
            messages=[{"role": "system", "content": "You are a fitness assistant.dont give answer to any other questions unrelated to fitness AND give response in div formate"}, 
                      {"role": "user", "content": user_input}]
        )
        bot_response = response["choices"][0]["message"]["content"]
        #bot_response=bot_response.split("```html")[1]
        #bot_response=bot_response.split("```")[0]
        
        return JsonResponse({"response": bot_response})

    return JsonResponse({"response": "Invalid request."})
