<?php
// Démarrer la session (ou simuler)
session_start();

// Définir un nom d'utilisateur par défaut pour la simulation
if (!isset($_SESSION['username'])) {
    $_SESSION['username'] = 'Attaquant';
}

// CSS intégré pour le rendu esthétique
$PAGE_STYLE = '
<style>
    body { font-family: "Arial", sans-serif; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    h2, h3 { color: #34495e; }
    form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
    input[type="text"] { 
        width: 100%; padding: 10px; margin: 8px 0; display: inline-block; 
        border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; 
    }
    input[type="submit"] { 
        background-color: #f39c12; color: white; padding: 10px 20px; 
        border: none; border-radius: 4px; cursor: pointer; font-size: 16px;
    }
    input[type="submit"]:hover { background-color: #e67e22; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    .success { color: #27ae60; font-weight: bold; }
</style>
';

$message = "";

// Logique de changement de nom d'utilisateur
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['new_username'])) {
    $new_username = $_POST['new_username'];
    
    // ⚠️ VULNÉRABILITÉ CSRF ⚠️ : Aucune vérification de jeton CSRF n'est effectuée ici.
    $_SESSION['username'] = htmlspecialchars($new_username);
    $message = "<p class='success'>SUCCESS: Le nom d'utilisateur a été changé en: <strong>" . $_SESSION['username'] . "</strong></p>";
}

?>
<!DOCTYPE html>
<html>
<head>
    <title>CSRF Lab</title>
    <?php echo $PAGE_STYLE; ?>
</head>
<body>
    <div class="vulnerability-note">VULNÉRABILITÉ: Cross-Site Request Forgery (CSRF) - Port 8084</div>
    <h1>CSRF Lab - Page de Profil Utilisateur</h1>

    <h2>Votre Profil</h2>
    <p>Nom d'utilisateur actuel: <strong><?php echo htmlspecialchars($_SESSION['username']); ?></strong></p>
    <?php echo $message; ?>

    <hr>

    <h2>Changer le Nom d'Utilisateur (Vulnérable)</h2>
    <p>Cette action ne vérifie pas l'origine de la requête.</p>
    
    <form method="POST" action="index.php">
        <label for="new_username">Nouveau Nom d'Utilisateur:</label>
        <input type="text" id="new_username" name="new_username" required>
        <input type="submit" value="Mettre à Jour le Nom">
    </form>
    
    <hr>
    
    <h2>Instructions pour le CSRF</h2>
    <p>Créez un formulaire caché sur une page externe (ex: un site d'attaque) qui pointe vers cette URL (<code>http://localhost:8084/</code>) avec les mêmes paramètres POST. Lorsque l'utilisateur visite le site d'attaque, la requête sera exécutée ici.</p>

</body>
</html>
