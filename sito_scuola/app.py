from flask import Flask, render_template, request, jsonify, abort
from difflib import get_close_matches

app = Flask(__name__)

# Dizionario delle risposte con parole chiave
responses = {
    "Quando è stato inventato il pallone di Gravina?": "Il pallone di Gravina ha origine nel 1859.",
    "Che sapore ha?": "Il sapore del pallone di Gravina cambia a secondo della stagionatura vede evolvere i sapori da semplici,del latte fresco,a complessi.",
    "tradizione": "Il Pallone di Gravina è una tradizione antica che ha radici nel passato storico della città, tramandata da generazioni.",
    "Quanto costa il pallone di Gravina?": "Il costo di un pallone di Gravina si aggira tra i 9,90€ e i 35,00€.",
    "Dove si produce il pallone di Gravina?": "Il pallone di gravina viene prodotto a gravina nelle cantine di calcarinite di Gravina, grotte di roccia della Murgia pugliese.",
    "Che forma ha il pallone di gravina?": "Il pallone di Gravina ha una forma di un cerchio ,come suggerisce il nome.",
    "formaggio_caciocavallo": "Il Caciocavallo è un formaggio dalla pasta filata che prende il nome dalla sua forma, che ricorda quella di una palla appesa.",
    "cultura": "La cultura di Gravina è molto legata alle tradizioni agricole e artigianali, con un forte senso di comunità.",
    "storia_pallone_di_gravina": "La storia del Pallone di Gravina risale al periodo medievale e rappresenta una parte importante della cultura di questa città."
}

def get_similar_questions(query, n=3):
    return get_close_matches(query.lower(), list(responses.keys()), n=n, cutoff=0.6)

def respond_to_query(query):
    query = query.lower()
    
    for keyword, response in responses.items():
        if keyword.replace('_', ' ') in query:
            similar = get_similar_questions(query)
            return response, [k.replace('_', ' ') for k in similar if k != keyword]
    
    similar = get_similar_questions(query)
    if similar:
        return responses[similar[0]], [k.replace('_', ' ') for k in similar[1:]]
    
    return "Mi dispiace, non ho una risposta specifica per questa domanda. Prova a riformularla.", []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/<page>")
def render_page(page):
    try:
        return render_template(f"{page}.html")
    except:
        return render_template("404.html"), 404

@app.route("/ai", methods=["POST"])
def ai():
    try:
        user_query = request.form.get("query", "").strip()
        if not user_query:
            return jsonify({
                "error": "La domanda non può essere vuota",
                "suggestions": list(responses.keys())[:3]
            }), 400
            
        response, suggestions = respond_to_query(user_query)
        return jsonify({
            "response": response,
            "suggestions": suggestions
        })
    except Exception as e:
        return jsonify({
            "error": "Si è verificato un errore",
            "suggestions": []
        }), 500

if __name__ == "__main__":
    app.run(debug=True)