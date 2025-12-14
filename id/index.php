<?php
// CSS intégré
$PAGE_STYLE = '
<style>
    body { font-family: "Arial", sans-serif; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    h2, h3 { color: #34495e; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    .status { margin-top: 15px; font-weight: bold; }
    code { background: #ecf0f1; padding: 2px 5px; border-radius: 3px; }
</style>
';

$message = "";

// 1. DÉFINITION DE LA CLASSE DE GESTION VULNÉRABLE (Gadget Chain Simulé)
class UserPrefs {
    public $filename;
    public $data;

    // La fonction __destruct() est appelée automatiquement lorsque l'objet est détruit (fin de la requête ou garbage collection).
    // Elle est la cible de l'attaque par désérialisation.
    function __destruct() {
        if (isset($this->filename) && isset($this->data)) {
            // ⚠️ VULNÉRABILITÉ : Utilisation d'une fonction dangereuse avec des données non fiables.
            file_put_contents($this->filename, $this->data);
            global $message;
            $message = "<p class='status success'>DEBUG: Fichier '{$this->filename}' écrit avec succès (ou non) par le gadget chain!</p>";
        }
    }
}

// 2. LOGIQUE VULNÉRABLE DE DÉSÉRIALISATION
if (isset($_COOKIE['user_prefs'])) {
    $serialized_data = base64_decode($_COOKIE['user_prefs']);
    
    // ⚠️ VULNÉRABILITÉ INSECURE DESERIALIZATION ⚠️ : Appel non sécurisé de unserialize()
    // Si l'attaquant fournit un objet UserPrefs sérialisé, la fonction __destruct() sera appelée.
    $user = @unserialize($serialized_data);
    
    if ($user === false) {
        $message = "<p class='status error'>ERROR: Données de cookie non valides (Désérialisation échouée).</p>";
    } else {
        $message .= "<p class='status success'>SUCCESS: Préférences utilisateur chargées.</p>";
    }
} else {
    // Si pas de cookie, définir un cookie par défaut (non dangereux)
    $default_prefs = serialize(['theme' => 'light', 'lang' => 'en']);
    setcookie('user_prefs', base64_encode($default_prefs));
    $message = "<p class='status'>INFO: Cookie par défaut créé. Rechargez la page.</p>";
}

?>
<!DOCTYPE html>
<html>
<head>
    <title>Insecure Deserialization Lab</title>
    <?php echo $PAGE_STYLE; ?>
</head>
<body>
    <div class="vulnerability-note">VULNÉRABILITÉ: Insecure Deserialization / RCE - Port 8089</div>
    <h1>Lab Insecure Deserialization</h1>

    <p>Cette application utilise le cookie <code>user_prefs</code>, qui est sérialisé, pour stocker les préférences utilisateur.</p>
    
    <h2>État de la Requête</h2>
    <?php echo $message; ?>

    <hr>
    
    <h3>Instructions pour l'Attaque</h3>
    <p><strong>Cible :</strong> Exploiter la classe <code>UserPrefs</code> pour écrire un fichier arbitraire (un shell PHP) sur le serveur, menant au RCE.</p>
    <p>1. Le cookie <code>user_prefs</code> contient des données <code>base64_encode(serialize(...))</code>.</p>
    <p>2. Créez un objet de la classe <code>UserPrefs</code> en définissant <code>$filename</code> (ex: <code>shell.php</code>) et <code>$data</code> (ex: <code>&lt;?php system($_GET['cmd']); ?&gt;</code>).</p>
    <p>3. Sérialisez cet objet, Base64-encodez-le, puis remplacez la valeur du cookie.</p>
    <p>4. La fonction <code>__destruct()</code> sera appelée, et votre shell sera écrit sur le serveur.</p>

    <hr>
    
    <h3>Exemple de Sérialisation (non malveillante)</h3>
    <p>Cookie actuel (base64) : <code><?php echo htmlspecialchars($_COOKIE['user_prefs'] ?? 'N/A'); ?></code></p>
    <p>Cookie décodé (sérialisé) : <code><?php echo htmlspecialchars($serialized_data ?? 'N/A'); ?></code></p>


</body>
</html>
