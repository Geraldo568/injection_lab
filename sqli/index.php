<?php
// Configuration from docker-compose.yml
$servername = "mysql_db";
$username = "appuser";
$password = "apppassword";
$dbname = "sqli_db";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$message = "Welcome to the Blind Login. Please enter your credentials.";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $input_user = $_POST['username'];
    $input_pass = $_POST['password'];

    // Expert Filter: Forcing use of alternative techniques
    $input_user = str_ireplace(['union', 'select', 'sleep', 'benchmark', ' '], ['','','','','/**/'], $input_user);
    $input_pass = str_ireplace(['union', 'select', 'sleep', 'benchmark', ' '], ['','','','','/**/'], $input_pass);

    $sql = "SELECT id FROM users WHERE username = '" . $input_user . "' AND password = SHA2('" . $input_pass . "', 256)";

    // Use query() instead of prepared statements for vulnerability
    $result = $conn->query($sql);
    
    // The application always provides the same message, regardless of login success
    $message = "Login attempt processed.";

    // Internal success check (no output difference)
    if ($result && $result->num_rows > 0) {
        error_log("SUCCESS! User '" . $input_user . "' logged in.");
    }
}
?>
<!DOCTYPE html>
<html>
<head><title>Blind SQLi Lab</title></head>
<style>
    body { font-family: 'Arial', sans-serif; background-color: #f4f4f9; color: #333; margin: 20px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
    h2, h3 { color: #34495e; }
    form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }
    input[type="text"], input[type="password"] { 
        width: 100%; padding: 10px; margin: 8px 0; display: inline-block; 
        border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; 
    }
    input[type="submit"] { 
        background-color: #3498db; color: white; padding: 10px 20px; 
        border: none; border-radius: 4px; cursor: pointer; font-size: 16px;
    }
    input[type="submit"]:hover { background-color: #2980b9; }
    pre { background: #ecf0f1; border: 1px solid #bdc3c7; padding: 15px; border-radius: 4px; overflow-x: auto; white-space: pre-wrap; }
    .vulnerability-note { background-color: #f39c12; color: white; padding: 5px; border-radius: 4px; text-align: center; margin-bottom: 15px; }
    .success { color: green; font-weight: bold; }
    .error { color: red; font-weight: bold; }
</style>
<body>
    <h1>Blind SQL Injection Lab (Port 8080)</h1>
    <p>Target: Find the hash of the 'admin' password using time-based blind injection.</p>
    <p>**Filter Bypass Required:** Common keywords are filtered. You must use alternative delay techniques and context.</p>
    <hr>
    <p><?php echo $message; ?></p>
    <form method="POST">
        Username: <input type="text" name="username" value="admin"><br>
        Password: <input type="password" name="password" value="pass"><br>
        <button type="submit">Login</button>
    </form>
</body>
</html>
