<?php
// Simule un proxy qui accepte les requêtes POST
// ⚠️ VULNÉRABILITÉ HTTP REQUEST TUNNELING ⚠️
// Le WAF ne scanne que la première ligne et les premiers en-têtes.
// Une requête complète peut être cachée dans le corps d'une requête POST.

$is_admin_accessible = ($_SERVER['REMOTE_ADDR'] === '127.0.0.1');

$PAGE_STYLE = '
<style>
    body { font-family: "Arial", sans-serif; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    pre { background: #ecf0f1; border: 1px solid #bdc3c7; padding: 15px; border-radius: 4px; overflow-x: auto; white-space: pre-wrap; }
    .info { color: #3498db; margin-top: 15px; }
</style>
';

$output = "";

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $raw_post_data = file_get_contents("php://input");
    
    $output = "Contenu POST reçu (première requête scannée et acceptée) :\n\n" . htmlspecialchars($raw_post_data);
    
    // Simuler le Backend qui traite le corps comme une nouvelle requête à tunneliser
    if (strpos($raw_post_data, "GET /admin.php") !== false) {
        $output .= "\n\n--- Tunnel Détecté ---\n";
        $output .= "Le Backend a traité une requête cachée : GET /admin.php";
        
        if ($is_admin_accessible) {
            $output .= "\n\n" . file_get_contents("http://127.0.0.1/admin.php");
        } else {
            $output .= "\n\n(L'accès admin n'est pas configuré pour localhost dans ce simulateur PHP)";
        }
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>HTTP Request Tunneling Lab</title>
    <?php echo $PAGE_STYLE; ?>
</head>
<body>
    <div class="vulnerability-note">VULNÉRABILITÉ: HTTP Request Tunneling (Abus H2.TE) - Port 8111</div>
    <h1>Lab 32 - Endpoint de Traitement POST (Vulnérable)</h1>

    <p>Ce point d'entrée est censé être un simple traitement POST. Cependant, le Backend (simulé) est vulnérable au "tunneling" où une requête HTTP complète est cachée dans le corps de données.</p>
    
    <h3>Instructions pour l'Attaque</h3>
    <p><strong>Cible :</strong> Accéder à la page interne <code>/admin.php</code> qui n'est accessible que depuis `localhost`.</p>
    <p>1. Envoyez une requête POST à <code>http://localhost:8111/</code>.</p>
    <p>2. Le corps de la requête POST doit contenir une requête HTTP complète, immédiatement après les en-têtes de la première requête. L'idée est de *cacher* la requête `/admin.php` dans les données POST.</p>
    
    <p>Charge Utile (Envoyée dans le corps du POST) :</p>
    <pre>
data=payload&x=y

GET /admin.php HTTP/1.1
Host: localhost
X-Tunnel: true
</pre>
    <p>3. Le Backend interprète ceci comme deux requêtes (la première est la requête POST légitime, la seconde est la requête tunnelée). Si le Backend est configuré pour penser que cette seconde requête provient de lui-même (via le tunnel), l'accès admin réussit.</p>

    <h2>Résultat de la Requête POST</h2>
    <pre><?php echo $output; ?></pre>
</body>
</html>
