<?php

// Zoom API credentials
$zoom_api_key = 'YOUR_ZOOM_API_KEY';
$zoom_api_secret = 'YOUR_ZOOM_API_SECRET';

// Generate a random 8-character alphanumeric string for the meeting topic
$meeting_topic = substr(str_shuffle('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'), 0, 8);

// Create a new Zoom meeting
$data = array(
    'topic' => $meeting_topic,
    'type' => 2,
    'password' => substr(str_shuffle('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'), 0, 8)
);

$options = array(
    'http' => array(
        'method' => 'POST',
        'header' => 'Authorization: Bearer ' . generate_jwt_token($zoom_api_key, $zoom_api_secret) . "\r\n" .
                    'Content-Type: application/json' . "\r\n",
        'content' => json_encode($data)
    )
);

$context = stream_context_create($options);
$result = file_get_contents('https://api.zoom.us/v2/users/me/meetings', false, $context);
$response = json_decode($result);

// Retrieve the meeting ID and password
$zoom_id = $response->id;
$zoom_password = $response->password;

// Generate a JWT token for Zoom API authentication
function generate_jwt_token($api_key, $api_secret) {
    $time = time();
    $payload = array(
        'iss' => $api_key,
        'exp' => $time + 60,
        'iat' => $time
    );
    $header = array(
        'alg' => 'HS256',
        'typ' => 'JWT'
    );
    $base64_header = base64_encode(json_encode($header));
    $base64_payload = base64_encode(json_encode($payload));
    $signature = hash_hmac('sha256', "$base64_header.$base64_payload", $api_secret, true);
    $base64_signature = base64_encode($signature);
    return "$base64_header.$base64_payload.$base64_signature";
}

?>