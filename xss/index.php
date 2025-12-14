<?php
// CSS intégré pour le rendu esthétique
$PAGE_STYLE = '
<style>
    body { font-family: "Arial", sans-serif; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    h2, h3 { color: #34495e; }
    form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
    input[type="text"], textarea { 
        width: 100%; padding: 10px; margin: 8px 0; display: inline-block; 
        border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; 
    }
    input[type="submit"] { 
        background-color: #2ecc71; color: white; padding: 10px 20px; 
        border: none; border-radius: 4px; cursor: pointer; font-size: 16px;
    }
    input[type="submit"]:hover { background-color: #27ad60; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    .comment-box { border: 1px solid #ccc; padding: 10px; margin-top: 10px; background-color: #fff; border-radius: 4px; }
    .comment-box p { margin: 0; }
</style>
';

// --- LOGIQUE XSS STOCKED ---
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['comment'])) {
    $comment = $_POST['comment'];
    $file = 'comments.txt';
    // ⚠️ VULNÉRABILITÉ XSS STOCKED ⚠️ : Écriture directe du commentaire non filtré
    file_put_contents($file, $comment . "\n", FILE_APPEND | LOCK_EX);
}
// --- FIN LOGIQUE XSS STOCKED ---

$page_content = '
    <div class="vulnerability-note">VULNÉRABILITÉ: Cross-Site Scripting (XSS) - Reflected, Stored, DOM (Port 8083)</div>
    
    <h1>XSS Lab</h1>

    <h2>1. Reflected XSS (GET parameter)</h2>
    <p>Ce champ reflète l\'entrée non filtrée dans le HTML.</p>
    <form method="GET">
        <label for="search">Recherche:</label>
        <input type="text" name="search" value="">
        <input type="submit" value="Search">
    </form>
';

// ⚠️ VULNÉRABILITÉ XSS REFLECTED ⚠️ : Le paramètre 'search' est affiché sans htmlspecialchars()
if (isset($_GET['search'])) {
    $search = $_GET['search'];
    $page_content .= '<h3>Résultats de recherche pour : ' . $search . '</h3>'; // <-- INJECTION POSSIBLE ICI
} else {
    $page_content .= '<h3>Entrez un terme de recherche dans le champ ci-dessus.</h3>';
}

$page_content .= '
    <hr>
    <h2>2. Stored XSS (Commentaires)</h2>
    <p>Laissez un commentaire. Il sera stocké et affiché à tous les visiteurs.</p>
    <form method="POST">
        <label for="comment">Votre Commentaire:</label>
        <textarea name="comment" rows="3"></textarea>
        <input type="submit" value="Submit Comment">
    </form>
    
    <h3>Commentaires Récents (Vulnérables)</h3>
';

// Affichage des commentaires (XSS STOCKED)
$comments = file('comments.txt', FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
if ($comments) {
    foreach ($comments as $comment) {
        // ⚠️ VULNÉRABILITÉ XSS STOCKED ⚠️ : Affichage direct du contenu du fichier
        $page_content .= '<div class="comment-box">' . $comment . '</div>'; 
    }
} else {
    $page_content .= '<p>Aucun commentaire pour l\'instant.</p>';
}

$page_content .= '
    <hr>
    <h2>3. DOM XSS (Client-Side)</h2>
    <p>Le JavaScript client récupère un paramètre de l\'URL (fragment <code>#lang=...</code>) et le manipule de manière non sécurisée. Testez avec <code>#lang=&lt;img src=x onerror=alert(1)&gt;</code></p>
    
    <div id="language-display"></div>

    <script>
        // ⚠️ VULNÉRABILITÉ DOM XSS ⚠️
        const url = new URL(window.location.href);
        const hash = url.hash.substring(1); 
        
        if (hash) {
            const params = new URLSearchParams(hash);
            const lang = params.get("lang");
            
            if (lang) {
                // INJECTION DANS innerHTML SANS FILTRE
                document.getElementById("language-display").innerHTML = "Langue sélectionnée (Vulnérable) : " + lang;
            }
        }
    </script>
';
?>
<!DOCTYPE html>
<html>
<head>
    <title>XSS Injection Lab</title>
    <?php echo $PAGE_STYLE; ?>
</head>
<body>
    <?php echo $page_content; ?>
</body>
</html>
