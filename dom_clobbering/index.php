<?php
$PAGE_STYLE = '
<style>
    body { font-family: "Arial", sans-serif; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    .info { color: #3498db; margin-top: 15px; }
</style>
';

// Récupérer la charge utile potentielle
$payload = $_GET['payload'] ?? 'Cliquez sur le bouton de test.';

?>
<!DOCTYPE html>
<html>
<head>
    <title>DOM Clobbering Lab</title>
    <?php echo $PAGE_STYLE; ?>
</head>
<body>
    <div class="vulnerability-note">VULNÉRABILITÉ: XSS via DOM Clobbering - Port 8099</div>
    <h1>Lab 20 - Désinfectant de Script Côté Client</h1>

    <p>Cette application utilise une variable JavaScript globale nommée <code>data</code> pour stocker le contenu à désinfecter avant de l'afficher.</p>

    <div id="content_display" style="border: 1px solid #ccc; padding: 15px;">
        Contenu affiché ici après désinfection.
    </div>

    <script>
        // ⚠️ VULNÉRABILITÉ DOM CLOBBERING ⚠️
        // Cette variable globale sera écrasée si un élément HTML avec id="data" est injecté.
        // Un objet DOM n'est pas une chaîne et le script plante/s'exécute mal.
        var data = '<?php echo $payload; ?>';

        // Fonction de désinfection (simplifiée pour le lab)
        function sanitizeAndDisplay(inputData) {
            // Dans un scénario réel, des filtres JS complexes s'appliqueraient ici.
            // S'ils s'attendent à ce que 'inputData' soit une chaîne, l'écraser avec un objet DOM 
            // causera une erreur ou un contournement.
            
            if (typeof inputData !== 'string' || inputData.includes('<script>')) {
                document.getElementById('content_display').innerHTML = '<span style="color: red;">[Protection] Script bloqué ou variable écrasée.</span>';
                return;
            }
            
            document.getElementById('content_display').innerHTML = inputData;
        }
        
        // Exécuter l'affichage
        sanitizeAndDisplay(data);

        // Cette partie est la cible de l'attaque. Si l'attaquant peut injecter un élément DOM
        // qui fait référence à la variable 'data', il peut potentiellement la manipuler.
        // Dans ce lab, nous nous concentrons sur l'écrasement pur.
    </script>
    
    <hr>
    
    <h3>Instructions pour l'Attaque</h3>
    <p><strong>Cible :</strong> Exécuter un XSS malgré les filtres JavaScript.</p>
    <p>1. Injectez un élément HTML dans le paramètre <code>payload</code> qui écrasera la variable globale <code>data</code>.</p>
    <p>Charge utile type (ID Clobbering) :</p>
    <p><code>&lt;a id="data" href="javascript:alert('CLOBBERED')"&gt;CLICK&lt;/a&gt;</code></p>
    <p>2. L'URL d'attaque serait (URL-encodée) :</p>
    <p><code>http://localhost:8099/?payload=&lt;a%20id="data"%20href="javascript:alert('CLOBBERED')"&gt;CLICK&lt;/a&gt;</code></p>
    <p>3. Lorsque le JavaScript s'exécute, `data` pointe maintenant vers l'élément `&lt;a&gt;`. Le code de désinfection reçoit un objet DOM au lieu d'une chaîne, et peut planter ou contourner la vérification de chaîne, affichant l'objet `&lt;a&gt;` qui est lui-même une charge utile.</p>

</body>
</html>
