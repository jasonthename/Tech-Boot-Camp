from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import wikipedia

app = Flask(__name__)
wikipedia.set_lang("en")

@app.route("/whatsapp", methods=['POST'])
def whatsapp_bot():
    incoming_msg = request.form.get('Body', '').strip()
    print(f"[User]: {incoming_msg}")

    resp = MessagingResponse()
    msg = resp.message()

    try:
        search_results = wikipedia.search(incoming_msg)
        print(f"[Search results]: {search_results}")

        if not search_results:
            msg.body("No matching Wikipedia article found.")
            return str(resp)

        # Try to directly get the first page's summary safely
        for title in search_results:
            try:
                print(f"Trying page: {title}")
                page = wikipedia.page(title, auto_suggest=False, preload=False)
                summary = page.summary[:1000]  # Truncate to avoid WhatsApp cutoff
                msg.body(summary)
                return str(resp)
            except wikipedia.exceptions.DisambiguationError as e:
                print(f"[DisambiguationError]: {title} → {e.options[:5]}")
                continue
            except wikipedia.exceptions.PageError:
                print(f"[PageError]: No page for {title}")
                continue
            except Exception as e:
                print(f"[Unexpected error]: {e}")
                continue

        msg.body("Still couldn't find a valid Wikipedia article. Try again with something else.")
    except Exception as e:
        print(f"[Outer Exception]: {e}")
        msg.body(f"Something went wrong: {str(e)}")

    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)
