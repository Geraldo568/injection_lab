<?php
// CSS intégré pour le rendu esthétique
$PAGE_STYLE = '
<style>
    body { font-family: "Arial", sans-serif; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    h2, h3 { color: #34495e; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    .action-zone { 
        background: #fff; 
        padding: 50px; 
        border-radius: 8px; 
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2); 
        text-align: center;
        margin-top: 50px;
        position: relative;
    }
    .action-button {
        background-color: #c0392b; /* Rouge dangereux */
        color: white;
        padding: 15px 30px;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-size: 18px;
        font-weight: bold;
        transition: background-color 0.3s;
    }
    .action-button:hover {
        background-color: #a02d20;
    }
</style>
';

$message = "";

// Logique pour la "suppression"
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['action']) && $_POST['action'] == 'delete') {
    // ⚠️ VULNÉRABILITÉ ⚠️: Le bouton exécute une action dangereuse
    $message = "<h2 style='color: #c0392b;'>SUCCESS: Le compte utilisateur (simulé) a été SUPPRIMÉ !</h2>";
}

?>
<!DOCTYPE html>
<html>
<head>
    <title>Clickjacking Lab - Cible</title>
    <?php echo $PAGE_STYLE; ?>
</head>
<body>
    <div class="vulnerability-note">VULNÉRABILITÉ: Clickjacking / UI Redressing (Port 8085)</div>
    <h1>Lab Clickjacking - Page d'Action Dangereuse</h1>

    <?php echo $message; ?>
    
    <div class="action-zone">
        <h2>Zone d'Action Critique</h2>
        <p>Cliquez sur ce bouton si vous êtes sûr de vouloir continuer.</p>
        
        <form method="POST" action="index.php">
            <input type="hidden" name="action" value="delete">
            <input type="submit" value="Supprimer Définitivement le Compte" class="action-button">
        </form>
        
    </div>

    <hr>
    
    <h2>Instructions (Site Attaquant)</h2>
    <p>Pour exploiter cette faille, vous devez créer une page sur un autre port (ou serveur) qui utilise une <code>&lt;iframe&gt;</code> pour charger cette page, puis la masquer avec <code>opacity: 0.001</code> et la placer exactement au-dessus d'un leurre visuel. Cette page est vulnérable car elle n'envoie PAS d'entête <code>X-Frame-Options: DENY</code>.</p>
</body>
</html>
