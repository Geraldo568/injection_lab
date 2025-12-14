<?php
// CSS intégré pour le rendu esthétique
$PAGE_STYLE = '
<style>
    body { font-family: "Arial", sans-serif; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    h2, h3 { color: #34495e; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    .document-box { background: #fff; padding: 20px; border: 1px solid #ccc; border-radius: 6px; margin-top: 15px; }
    .owner { font-style: italic; color: #3498db; }
    .secret { color: #c0392b; font-weight: bold; }
</style>
';

// Données Simulant la Base de Données
// user_id est la clé qui devrait être vérifiée!
$documents = [
    1 => [
        'id' => 101,
        'user_id' => 1,
        'title' => 'Mon Document Personnel 101',
        'content' => 'Ceci est mon document privé. Flag: Flag{IDOR_user_1_document_101}',
        'owner' => 'User A (ID 1)'
    ],
    2 => [
        'id' => 202,
        'user_id' => 2,
        'title' => 'Document Secret du PDG 202',
        'content' => 'Ce document contient des informations confidentielles. Flag: Flag{IDOR_PDG_secret_access}',
        'owner' => 'User B (PDG - ID 2)'
    ]
];

// Simuler que l'utilisateur connecté est toujours l'ID 1
$CURRENT_USER_ID = 1;
$CURRENT_USER_NAME = 'User A (Attaquant)';

$document_id = isset($_GET['doc_id']) ? intval($_GET['doc_id']) : 101;
$document_found = false;
$output = "";

// Rechercher le document
foreach ($documents as $doc) {
    if ($doc['id'] === $document_id) {
        $document_found = true;
        
        // ⚠️ VULNÉRABILITÉ IDOR ⚠️: Aucune vérification n'est faite pour s'assurer que $doc['user_id'] == $CURRENT_USER_ID
        // L'attaquant peut simplement changer ?doc_id=101 à ?doc_id=202
        
        $output .= "<div class='document-box'>";
        $output .= "<h2>" . htmlspecialchars($doc['title']) . " (ID: " . $doc['id'] . ")</h2>";
        $output .= "<p class='owner'>Propriétaire: " . htmlspecialchars($doc['owner']) . "</p>";
        $output .= "<p>Contenu: <span class='secret'>" . htmlspecialchars($doc['content']) . "</span></p>";
        
        if ($doc['user_id'] === $CURRENT_USER_ID) {
            $output .= "<p style='color:green;'>-- ACCÈS LÉGITIME --</p>";
        } else {
            $output .= "<p style='color:red;'>-- L'utilisateur connecté n'est PAS le propriétaire de ce document! --</p>";
        }
        
        $output .= "</div>";
        break;
    }
}

if (!$document_found) {
    $output = "<p>Document non trouvé.</p>";
}

?>
<!DOCTYPE html>
<html>
<head>
    <title>IDOR Lab</title>
    <?php echo $PAGE_STYLE; ?>
</head>
<body>
    <div class="vulnerability-note">VULNÉRABILITÉ: Insecure Direct Object Reference (IDOR) - Port 8087</div>
    <h1>Lab IDOR - Lecteur de Documents</h1>

    <h2>Utilisateur Connecté: <?php echo $CURRENT_USER_NAME; ?></h2>
    <p>Cette page affiche un document basé sur le paramètre <code>?doc_id=...</code> dans l'URL.</p>
    
    <p>Essayez de changer l'URL pour accéder au document ID 202 (celui du PDG).</p>

    <hr>
    
    <h3>Document Affiché (ID: <?php echo $document_id; ?>)</h3>
    <?php echo $output; ?>

</body>
</html>
