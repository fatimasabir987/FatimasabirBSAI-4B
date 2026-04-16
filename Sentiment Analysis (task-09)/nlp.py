from textblob import TextBlob

print("--- AI Sentiment Analyzer System ---")
print("Type 'quit' to stop the program.\n")

while True:
    user_query = input("Ask me anything or enter a sentence to analyze: ")

    if user_query.lower() == 'quit':
        print("Exiting... Goodbye!")
        break

    analysis = TextBlob(user_query) 

    score = analysis.sentiment.polarity 

    if score > 0:
        result = "Positive"
    elif score < 0:
        result = "Negative"
    else:
        result = "Neutral"

    print(f">> Analysis: This sentence feels {result}.")
    print(f">> Confidence Score: {score}\n")



#Test Category, Example Question/Sentence,Expected Result
#Strong Positive, "This AI lab is the best experience ever!",Score >0.5 (Positive)
#Strong Negative, "I hate these errors, they are very annoying.",Score <−0.5 (Negative)
#Neutral, "There are four chairs in this classroom.",Score ≈0.0 (Neutral)
#Fact-based, "Python is a programming language.",Score ≈0.0 (Neutral)
