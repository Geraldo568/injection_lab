<?php
// Ressource secrète uniquement accessible via localhost ou un tunnel.
if ($_SERVER['REMOTE_ADDR'] === '127.0.0.1') {
    $content = "<span style='color: green;'>ACCÈS ADMINISTRATEUR RÉUSSI! Le secret est : H2TE-TUNNEL-4321.</span>";
} else {
    $content = "<span style='color: red;'>ACCÈS REFUSÉ. L'administration n'est accessible que depuis localhost. (Votre IP: " . $_SERVER['REMOTE_ADDR'] . ")</span>";
}
?>
<!DOCTYPE html><html><body><h1>Page Admin</h1><?php echo $content; ?></body></html>
