from flask import Flask, request, render_template_string, Response

app = Flask(__name__)

SMUGGLE_FLAG = "/tmp/hrs_smuggled_8124.txt"
FLAG_CONTENT = "HRS_SMUGGLING_SUCCESS"

@app.route('/process', methods=['POST'])
def process():
    # Simuler le rôle du Backend (utilisant Transfer-Encoding)
    
    # La vulnérabilité est ici : le backend lit jusqu'à la fin du chunk 
    # mais peut être trompé par un Content-Length envoyé par le frontend
    
    # Si la requête est normale
    if request.content_length and request.data:
        data = request.data.decode('utf-8')
        if "HRS_SMUGGLING_CHECK" in data:
             # C'est la signature de la requête "smuggled"
             import os
             if not os.path.exists(SMUGGLE_FLAG):
                 with open(SMUGGLE_FLAG, "w") as f:
                     f.write(FLAG_CONTENT)
                 return Response("Smuggling SUCCESS: Flag created.", status=200)
             else:
                 return Response("Smuggling already succeeded.", status=200)

        return Response(f"Backend processed normal data. Length: {len(request.data)}", status=200)
    
    return Response("Backend received unexpected data format (Smuggling likely).", status=400)

@app.route('/', methods=['GET'])
def index():
     return "Backend is running. Target: /process (POST)"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
