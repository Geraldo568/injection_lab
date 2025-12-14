<?php
// Simuler une application qui utilise X-Forwarded-Host pour générer un lien absolu.
// ⚠️ VULNÉRABILITÉ WCP ⚠️: Utilisation non sécurisée de l'en-tête X-Forwarded-Host.

$PAGE_STYLE = '
<style>
    body { font-family: "Arial", sans-serif; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    .poisoned-link { color: #c0392b; font-weight: bold; }
    .info { background: #ecf0f1; border: 1px solid #bdc3c7; padding: 15px; border-radius: 4px; }
</style>
';

// L'application est derrière un proxy qui définit cet en-tête
$host = $_SERVER['HTTP_X_FORWARDED_HOST'] ?? $_SERVER['HTTP_HOST'];

// En-têtes pour forcer la mise en cache par un proxy amont
header('Cache-Control: public, max-age=30'); 
header('Vary: Accept-Encoding'); // X-Forwarded-Host n'est PAS dans Vary

// ⚠️ Le host est inséré ici, permettant l'injection d'une charge utile XSS
$malicious_link = "https://{$host}/login.php"; 

?>
<!DOCTYPE html>
<html>
<head>
    <title>Web Cache Poisoning Lab</title>
    <?php echo $PAGE_STYLE; ?>
</head>
<body>
    <div class="vulnerability-note">VULNÉRABILITÉ: Web Cache Poisoning (WCP) - Port 8098</div>
    <h1>Lab 19 - Page d'Accueil mise en Cache</h1>

    <p>Cette page est mise en cache par un proxy (simulé par l'en-tête <code>Cache-Control: public</code>).</p>
    <p>Le lien de connexion est construit à l'aide de l'en-tête non-standard <code>X-Forwarded-Host</code>.</p>

    <h2>Lien de Connexion Généré</h2>
    <p>Le cache ne tient pas compte de l'en-tête <code>X-Forwarded-Host</code>, ce qui permet le WCP.</p>
    <div class="info">
        Lien absolu : <a href="<?php echo htmlspecialchars($malicious_link); ?>" class="poisoned-link">Cliquer ici pour se connecter</a>
    </div>

    <h3>Instructions pour l'Attaque</h3>
    <p><strong>Cible :</strong> Mettre en cache un lien malveillant pour les autres utilisateurs.</p>
    <p>1. Envoyez une requête à <code>http://localhost:8098/</code> avec un en-tête <code>X-Forwarded-Host</code> contenant une charge utile XSS ou une redirection vers votre site.</p>
    <p>Charge utile type (pour XSS si le `htmlspecialchars` est absent, ou une redirection de base) :<br>
    <code>X-Forwarded-Host: Attacker.com/</code></p>
    <p>2. Le proxy met en cache cette réponse malveillante.</p>
    <p>3. Les requêtes ultérieures des victimes recevront la réponse mise en cache, avec le lien pointant vers <code>https://Attacker.com/login.php</code>.</p>
</body>
</html>
