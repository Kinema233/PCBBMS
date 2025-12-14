<?php
header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode([
        'success' => false,
        'message' => 'Неприпустимий метод запиту.'
    ]);
    exit;
}

if (!isset($_FILES['dataFile']) || $_FILES['dataFile']['error'] !== UPLOAD_ERR_OK) {
    echo json_encode([
        'success' => false,
        'message' => 'Помилка завантаження файлу.'
    ]);
    exit;
}

$allowedExt = ['csv'];
$ext = strtolower(pathinfo($_FILES['dataFile']['name'], PATHINFO_EXTENSION));
if (!in_array($ext, $allowedExt)) {
    echo json_encode([
        'success' => false,
        'message' => 'Дозволено завантажувати тільки CSV-файли.'
    ]);
    exit;
}

$uploadDir = __DIR__ . '/uploads';
if (!is_dir($uploadDir)) {
    mkdir($uploadDir, 0777, true);
}

$targetPath = $uploadDir . '/uploaded_data.csv';

if (!move_uploaded_file($_FILES['dataFile']['tmp_name'], $targetPath)) {
    echo json_encode([
        'success' => false,
        'message' => 'Не вдалося зберегти файл на сервері.'
    ]);
    exit;
}

echo json_encode([
    'success' => true,
    'message' => 'Файл успішно завантажено.',
    'filename' => 'uploaded_data.csv'
]);
