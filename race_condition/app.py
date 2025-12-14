from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# Simuler un solde utilisateur dans la mémoire (variable globale)
USER_BALANCE = 100
MAX_PRODUCT_PRICE = 60 
PRODUCT_ID = 123
FLAG_FILE = "/tmp/race_condition_flag_8120.txt"

def check_for_exploit():
    global USER_BALANCE
    if USER_BALANCE < -50: 
        if not os.path.exists(FLAG_FILE):
             with open(FLAG_FILE, "w") as f:
                f.write("RACE_CONDITION_SUCCESS:Overspent!")
        return True
    return False

# NOTE: Tout le template est maintenant STRICTEMENT formaté pour Jinja2 ({{ et }})
HTML_TEMPLATE = """
<style>
    body { font-family: Arial; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #3498db; border-bottom: 2px solid #2980b9; padding-bottom: 10px; }
    .vulnerability-note { background-color: #3498db; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    .balance-box { background: #ecf0f1; padding: 15px; border-radius: 4px; margin-top: 15px; }
    .result { margin-top: 20px; padding: 10px; border: 1px dashed #7f8c8d; }
    .error { color: #e74c3c; font-weight: bold; }
    .success { color: #2ecc71; font-weight: bold; }
</style>

<div class="vulnerability-note">VULNÉRABILITÉ CRITIQUE : Race Condition (Contournement de Limite) - Port 8120</div>
<h1>Lab 41 - Boutique Éphémère (Product ID: {{ product_id }})</h1>

<div class="balance-box">
    Solde actuel de l'utilisateur : <b>${{ user_balance }}</b><br>
    Prix du produit : <b>${{ product_price }}</b>
</div>

<p>
    L'objectif est d'acheter deux fois le produit (2 x $60 = $120) alors que votre solde n'est que de $100, en exploitant la Race Condition dans la fonction de transaction.
    Si vous y parvenez, le solde sera fortement négatif et le drapeau sera créé.
</p>

<form method="POST">
    <input type="hidden" name="product_id" value="{{ product_id }}">
    <input type="submit" value="Acheter le produit">
</form>

{% if message %}
    <div class="result">
        {{ message|safe }}
    </div>
{% endif %}
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    global USER_BALANCE
    message = None
    
    context = {
        'product_id': PRODUCT_ID,
        'user_balance': USER_BALANCE,
        'product_price': MAX_PRODUCT_PRICE,
        'message': None # Initialisation du message pour Jinja
    }
    
    if check_for_exploit():
        context['message'] = f"<p class='success'>RACE CONDITION RÉUSSIE : Le drapeau <code>{FLAG_FILE}</code> a été créé !</p>"
        return render_template_string(HTML_TEMPLATE, **context)

    if request.method == 'POST':
        product_id = request.form.get('product_id', type=int)
        
        if product_id == PRODUCT_ID:
            
            if USER_BALANCE >= MAX_PRODUCT_PRICE:
                
                import time
                time.sleep(0.1) # Fenêtre de vulnérabilité

                USER_BALANCE -= MAX_PRODUCT_PRICE
                context['user_balance'] = USER_BALANCE
                
                message = f"<p class='success'>Achat réussi ! Solde restant : ${USER_BALANCE}</p>"
                
                if check_for_exploit():
                    message += "<p class='success'>RACE CONDITION RÉUSSIE : Le drapeau a été créé !</p>"

            else:
                message = f"<p class='error'>Transaction échouée : Solde insuffisant (${USER_BALANCE}).</p>"
        else:
            message = f"<p class='error'>Produit inconnu.</p>"

    context['message'] = message
    return render_template_string(HTML_TEMPLATE, **context)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
