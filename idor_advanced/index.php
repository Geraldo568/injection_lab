<?php
// Simuler les identifiants d'objets pour différents utilisateurs
$OBJECTS = [
    "user_alice" => [
        "hash_private_001" => "Contenu du rapport privé d'Alice (Rapport 1).",
        "hash_private_002" => "Contenu du rapport privé d'Alice (Rapport 2)."
    ],
    "user_bob" => [
        "hash_private_003" => "Contenu du rapport privé de Bob (Rapport 3). [SECRET]",
        "hash_private_004" => "Contenu du rapport privé de Bob (Rapport 4)."
    ]
];

// Simuler l'utilisateur actuellement authentifié (Alice)
$CURRENT_USER = "user_alice";

$PAGE_STYLE = '
<style>
    body { font-family: "Arial", sans-serif; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    .report-content { background: #fff; border-left: 5px solid #3498db; padding: 15px; margin-top: 10px; white-space: pre-wrap; }
    .info { color: #3498db; }
</style>
';

$report_hash = $_GET['id'] ?? null;
$content = "Aucun rapport sélectionné.";

if ($report_hash) {
    // ⚠️ VULNÉRABILITÉ IDOR AVANCÉ ⚠️
    // L'application vérifie que l'ID existe, mais PAS que l'ID appartient à $CURRENT_USER.
    
    $found = false;
    $target_user = null;

    // Recherche de l'ID dans tous les utilisateurs (y compris l'attaquant lui-même)
    foreach ($OBJECTS as $user => $reports) {
        if (array_key_exists($report_hash, $reports)) {
            $content = $reports[$report_hash];
            $target_user = $user;
            $found = true;
            break;
        }
    }

    if (!$found) {
        $content = "Erreur: Le rapport '{$report_hash}' est introuvable.";
    } elseif ($target_user !== $CURRENT_USER) {
        // En mode vulnérable, cette vérification est absente ou ne fait rien.
        $content = "<span style='color: red;'>Rapport trouvé (Appartient à {$target_user}) :</span><br>" . $content;
    } else {
        $content = "<span style='color: green;'>Rapport trouvé (Vous appartient) :</span><br>" . $content;
    }
}

?>
<!DOCTYPE html>
<html>
<head>
    <title>IDOR Avancé Lab</title>
    <?php echo $PAGE_STYLE; ?>
</head>
<body>
    <div class="vulnerability-note">VULNÉRABILITÉ: Insecure Direct Object Reference (IDOR) Avancé - Port 8097</div>
    <h1>Lab 18 - Visualiseur de Rapports (Utilisateur: <?php echo $CURRENT_USER; ?>)</h1>

    <p>Cette application utilise des identifiants non-séquentiels (hashs) pour les rapports, mais oublie de vérifier la propriété.</p>

    <h2>Vos Rapports (Alice) :</h2>
    <ul>
        <li><a href="?id=hash_private_001">hash_private_001</a></li>
        <li><a href="?id=hash_private_002">hash_private_002</a></li>
    </ul>

    <h2>Rapports Cibles (Bob) :</h2>
    <p class="info">L'objectif est d'accéder au rapport secret de Bob en utilisant son hash connu.</p>
    <ul>
        <li><code>hash_private_003</code> (Cible Secrète)</li>
        <li><code>hash_private_004</code></li>
    </ul>
    
    <hr>
    
    <h2>Contenu du Rapport (ID: <?php echo $report_hash ?? "N/A"; ?>)</h2>
    <div class="report-content">
        <?php echo $content; ?>
    </div>
    
    <h3>Instructions pour l'Attaque</h3>
    <p>1. Cliquez sur l'un de vos propres rapports (`hash_private_001`).</p>
    <p>2. Modifiez l'URL dans la barre d'adresse pour tenter d'accéder au rapport de Bob :</p>
    <p><code>http://localhost:8097/?id=hash_private_003</code></p>

</body>
</html>
