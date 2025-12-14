<?php
// ⚠️ VULNÉRABILITÉ WCD ⚠️: La page rend du contenu sensible (Clé API)
// même lorsque l'URL de la requête contient une extension statique.

$PAGE_STYLE = '
<style>
    body { font-family: "Arial", sans-serif; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    .sensitive { color: #c0392b; font-weight: bold; border: 1px dashed #c0392b; padding: 10px; display: inline-block; }
    .info { color: #3498db; margin-top: 15px; }
</style>
';

// 1. Simuler une session utilisateur authentifiée
$USERNAME = "alice_attaquant";
$API_KEY = "AK-2025-CLOUDKEY-123456789"; 

// 2. Récupérer l'URL de la requête
$request_uri = $_SERVER['REQUEST_URI'];

// 3. En-têtes pour simuler une mise en cache agressive
header('Cache-Control: public, max-age=3600');
header('Vary: Accept-Encoding'); // Important pour le cache

?>
<!DOCTYPE html>
<html>
<head>
    <title>Web Cache Deception Lab</title>
    <?php echo $PAGE_STYLE; ?>
</head>
<body>
    <div class="vulnerability-note">VULNÉRABILITÉ: Web Cache Deception (WCD) - Port 8094</div>
    <h1>Lab 15 - Page de Profil Authentifiée (Simulée)</h1>

    <p class="info">Vous êtes connecté en tant que <strong><?php echo $USERNAME; ?></strong>.</p>
    
    <h2>Informations Sensibles :</h2>
    <p>Cette clé ne devrait jamais être mise en cache par le Proxy.</p>
    <p>Clé API Privée: <span class="sensitive"><?php echo $API_KEY; ?></span></p>

    <hr>
    
    <h3>Instruction pour l'Attaque</h3>
    <p><strong>Cible :</strong> Forcer le proxy à mettre en cache la clé API de l'utilisateur.</p>
    <p>1. Simulez l'envoi du lien à la victime (Alice). L'URL doit contenir une extension statique valide :</p>
    <p><code>http://localhost:8094/profile/alice_sensible_data<strong>.css</strong></code></p>
    <p>2. Le serveur web ignore le <code>.css</code> et renvoie cette page (avec la clé API).</p>
    <p>3. Le Proxy Cache voit le <code>.css</code>, et met en cache **le contenu entier de cette page** pour cette URL.</p>
    <p>4. L'attaquant accède ensuite à la même URL <code>http://localhost:8094/profile/alice_sensible_data.css</code> et récupère la clé mise en cache.</p>

</body>
</html>
