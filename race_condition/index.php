<?php
$LIMIT_FILE = 'user_limit.txt';
$MAX_PURCHASE = 1;
$PAGE_STYLE = '
<style>
    body { font-family: "Arial", sans-serif; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    .status { margin-top: 15px; font-weight: bold; }
    .success { color: #27ae60; }
    .error { color: #c0392b; }
    .info { color: #3498db; }
    .limit { font-size: 1.2em; font-weight: bold; }
</style>
';

$message = "";
$current_count = 0;

// Lire la limite actuelle (Simule la lecture BDD)
if (file_exists($LIMIT_FILE)) {
    $data = file_get_contents($LIMIT_FILE);
    preg_match('/count:(\d+)/', $data, $matches);
    $current_count = isset($matches[1]) ? (int)$matches[1] : 0;
}

if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['action']) && $_POST['action'] == 'buy') {
    // ⚠️ VULNÉRABILITÉ RACE CONDITION ⚠️
    // Il y a un délai intentionnel qui augmente la fenêtre de course.
    sleep(1); 

    if ($current_count < $MAX_PURCHASE) {
        // Mise à jour (Simule l'écriture BDD)
        $new_count = $current_count + 1;
        
        // Cette écriture arrive APRÈS la lecture effectuée par la requête concurrente.
        file_put_contents($LIMIT_FILE, "count:$new_count");
        
        $message = "<p class='status success'>ACHAT RÉUSSI (Requête {$new_count}) : Vous avez maintenant {$new_count} article(s). (Max: $MAX_PURCHASE)</p>";
        $current_count = $new_count;
    } else {
        $message = "<p class='status error'>ACHAT ÉCHOUÉ : Vous avez déjà atteint la limite d'achat de {$MAX_PURCHASE}.</p>";
    }
} elseif ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['action']) && $_POST['action'] == 'reset') {
    file_put_contents($LIMIT_FILE, "count:0");
    $current_count = 0;
    $message = "<p class='status info'>Limite réinitialisée à 0.</p>";
}

?>
<!DOCTYPE html>
<html>
<head>
    <title>Race Condition Lab</title>
    <?php echo $PAGE_STYLE; ?>
</head>
<body>
    <div class="vulnerability-note">VULNÉRABILITÉ: Race Condition (RC) - Port 8093</div>
    <h1>Lab 14 - Limite d'Achat</h1>

    <p>Cette application vous permet d'acheter 1 article unique (Max: 1). La logique manque de mécanisme de **verrouillage transactionnel**.</p>
    
    <h2>État Actuel</h2>
    <p class="limit">Articles achetés : <?php echo $current_count; ?> / <?php echo $MAX_PURCHASE; ?></p>
    <?php echo $message; ?>

    <hr>
    
    <h2>Acheter un Article (avec la faille)</h2>
    <form action="" method="post">
        <input type="hidden" name="action" value="buy">
        <input type="submit" value="Acheter un Article (1s de délai)" style="background-color: #2ecc71;">
    </form>
    
    <h2>Réinitialiser la Limite</h2>
    <form action="" method="post">
        <input type="hidden" name="action" value="reset">
        <input type="submit" value="Réinitialiser" style="background-color: #3498db;">
    </form>
    
    <h3>Instructions pour l'Attaque</h3>
    <p><strong>Cible :</strong> Acheter 2 articles malgré la limite de 1.</p>
    <p>1. Assurez-vous que le compteur est à 0. Cliquez sur Réinitialiser si nécessaire.</p>
    <p>2. Utilisez un outil (Burp Intruder, cURL en parallèle, ou un script Python) pour envoyer **deux requêtes POST** d'achat au <code>http://localhost:8093/</code> **simultanément**.</p>
    <p>3. La première requête va lire 0, la seconde va lire 0. Les deux vont continuer et mettre à jour le compteur à 2.</p>

</body>
</html>
