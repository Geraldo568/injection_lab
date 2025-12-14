<?php
// Simuler la base de données
$ACCOUNTS = [
    'alice' => ['password' => 'hash_alice_pwd', 'email' => 'alice@example.com'],
    'bob' => ['password' => 'hash_bob_pwd', 'email' => 'bob@example.com']
];

$message = "";
$username = $_POST['username'] ?? '';
$action = $_POST['action'] ?? '';

$PAGE_STYLE = '
<style>
    body { font-family: "Arial", sans-serif; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
    input[type="text"], input[type="submit"] { padding: 10px; margin: 5px; border-radius: 4px; }
    .info { color: #3498db; margin-top: 15px; }
    .error { color: #c0392b; font-weight: bold; }
</style>
';

if ($action === 'reset_password' && $username) {
    if (isset($ACCOUNTS[$username])) {
        // Générer un jeton aléatoire (dans un vrai système)
        $reset_token = "RST-" . bin2hex(random_bytes(10));
        
        // ⚠️ VULNÉRABILITÉ TOKEN LEAK ⚠️
        // L'application est censée envoyer le token par email, mais le fuite
        // directement dans le corps de la réponse ou l'URL de redirection.
        
        $message = "<div class='info'>
            Un lien de réinitialisation a été envoyé à l'email de {$username}.<br>
            <span class='error'>[TOKEN FUITE]</span> Le lien de réinitialisation est visible ici (ou dans la redirection) :<br>
            <strong>http://localhost:8101/reset.php?token={$reset_token}</strong><br><br>
            L'attaquant doit trouver un moyen de faire exécuter à la victime la requête de réinitialisation, puis de lire le corps de cette réponse (via XSS, injection ou log).
        </div>";
        
        // Simuler un XSS stocké qui pourrait lire cette réponse
        // Si cette page est affichée sans filtre suite à une injection, le token est volé.
        
    } else {
        $message = "<p class='error'>Utilisateur non trouvé.</p>";
    }
}

?>
<!DOCTYPE html>
<html>
<head>
    <title>Token Leak Lab</title>
    <?php echo $PAGE_STYLE; ?>
</head>
<body>
    <div class="vulnerability-note">VULNÉRABILITÉ: Token Reset Leak - Port 8101</div>
    <h1>Lab 22 - Réinitialisation de Mot de Passe</h1>

    <p>Simule une faille où le jeton de réinitialisation est exposé au lieu d'être envoyé uniquement par email.</p>

    <form method="POST">
        <input type="hidden" name="action" value="reset_password">
        <label for="username">Nom d'utilisateur à réinitialiser (Ex: alice ou bob) :</label>
        <input type="text" id="username" name="username" required>
        <input type="submit" value="Réinitialiser le mot de passe">
    </form>
    
    <?php echo $message; ?>

    <h3>Instructions pour l'Attaque</h3>
    <p>1. Un attaquant (Alice) veut prendre le contrôle du compte de Bob (la victime).</p>
    <p>2. L'attaquant envoie la requête de réinitialisation pour "bob".</p>
    <p>3. Le serveur répond en divulguant l'URL du jeton (<code>RST-xxxxxxxxxx</code>) dans le corps de la réponse HTTP.</p>
    <p>4. L'attaquant récupère le jeton divulgué et l'utilise pour définir un nouveau mot de passe pour Bob (en simulant l'accès à <code>/reset.php?token=...</code>).</p>
</body>
</html>
