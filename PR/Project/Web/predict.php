<?php
header('Content-Type: application/json; charset=utf-8');

ini_set('display_errors', 1);
error_reporting(E_ALL);

$period = isset($_GET['period']) ? $_GET['period'] : 'all';
$daysLimit = ($period === 'all') ? null : (int)$period;

$filePath = __DIR__ . '/uploads/uploaded_data.csv';

if (!file_exists($filePath)) {
    echo json_encode([
        'success' => false,
        'message' => 'Файл з даними не знайдено. Спочатку завантажте CSV.'
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

$handle = fopen($filePath, 'r');
if ($handle === false) {
    echo json_encode([
        'success' => false,
        'message' => 'Не вдалося відкрити файл з даними.'
    ], JSON_UNESCAPED_UNICODE);
    exit;
}


$header = fgetcsv($handle, 0, ',');
if ($header === false) {
    echo json_encode([
        'success' => false,
        'message' => 'Не вдалося прочитати заголовок CSV.'
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

$required = ['client_id', 'client_name', 'purchase_date', 'product', 'category', 'quantity', 'price', 'total'];
$colIndex = array_flip($header);

foreach ($required as $col) {
    if (!isset($colIndex[$col])) {
        echo json_encode([
            'success' => false,
            'message' => 'У файлі немає обов’язкового стовпця: ' . $col
        ], JSON_UNESCAPED_UNICODE);
        exit;
    }
}

$rows = [];
$maxDate = null;

while (($row = fgetcsv($handle, 0, ',')) !== false) {
    if (count($row) < count($header)) {
        continue;
    }

    $dateStr = $row[$colIndex['purchase_date']];
    $dateTs  = strtotime($dateStr);
    if ($dateTs === false) {
        continue;
    }

    $rows[] = $row;

    if ($maxDate === null || $dateTs > $maxDate) {
        $maxDate = $dateTs;
    }
}

fclose($handle);

if (empty($rows)) {
    echo json_encode([
        'success' => false,
        'message' => 'У файлі немає валідних рядків з датою.'
    ], JSON_UNESCAPED_UNICODE);
    exit;
}


$clients = [];

foreach ($rows as $row) {
    $clientId   = $row[$colIndex['client_id']];
    $clientName = $row[$colIndex['client_name']];
    $dateStr    = $row[$colIndex['purchase_date']];
    $product    = $row[$colIndex['product']];
    $quantity   = (float)$row[$colIndex['quantity']];
    $total      = (float)$row[$colIndex['total']];

    $dateTs = strtotime($dateStr);
    if ($dateTs === false) {
        continue;
    }

    if ($daysLimit !== null) {
        if (($maxDate - $dateTs) > $daysLimit * 24 * 3600) {
            continue;
        }
    }

    if (!isset($clients[$clientId])) {
        $clients[$clientId] = [
            'id' => $clientId,
            'name' => $clientName,
            'purchases' => 0,
            'totalAmount' => 0.0,
            'lastPurchase' => $dateTs,
            'products' => []
        ];
    }

    $clients[$clientId]['purchases'] += 1;
    $clients[$clientId]['totalAmount'] += $total;

    if ($dateTs > $clients[$clientId]['lastPurchase']) {
        $clients[$clientId]['lastPurchase'] = $dateTs;
    }

    if (!isset($clients[$clientId]['products'][$product])) {
        $clients[$clientId]['products'][$product] = 0;
    }
    $clients[$clientId]['products'][$product] += $quantity;
}

if (empty($clients)) {
    echo json_encode([
        'success' => false,
        'message' => 'Після фільтрації періоду дані відсутні.'
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

function calcProbability($purchases, $totalAmount, $daysSinceLast)
{
    $freqScore   = min($purchases / 10.0, 1.0);
    $amountScore = min($totalAmount / 20000.0, 1.0);
    $recencyScore = exp(-$daysSinceLast / 365.0) * 0.9 + 0.1;

    $prob = (0.45 * $freqScore) + (0.35 * $amountScore) + (0.20 * $recencyScore);

    if ($prob > 1) $prob = 1;
    if ($prob < 0) $prob = 0;

    return $prob;
}

$result = [];
$totalProb = 0;
$highCount = 0;

foreach ($clients as $client) {
    $daysSinceLast = ($maxDate - $client['lastPurchase']) / (24 * 3600);

    $prob = calcProbability(
        $client['purchases'],
        $client['totalAmount'],
        $daysSinceLast
    );

    $totalProb += $prob;
    if ($prob >= 0.7) {
        $highCount++;
    }

    $recommendedProduct = '—';
    if (!empty($client['products'])) {
        arsort($client['products']);
        $keys = array_keys($client['products']);
        $recommendedProduct = $keys[0];
    }

    if ($prob >= 0.8) {
        $comment = 'Постійний клієнт з високою ймовірністю повернення. Рекомендовано персональні пропозиції.';
    } elseif ($prob >= 0.5) {
        $comment = 'Середня ймовірність повернення. Доцільно нагадати про акції та знижки.';
    } else {
        $comment = 'Низька активність. Можливі разові покупки, потрібна додаткова мотивація.';
    }

    $result[] = [
        'id'          => $client['id'],
        'name'        => $client['name'],
        'probability' => round($prob, 3),
        'recommended' => $recommendedProduct,
        'comment'     => $comment
    ];
}

$totalClients = count($clients);
$avgProb = $totalProb / max($totalClients, 1);

echo json_encode([
    'success' => true,
    'message' => 'Прогноз успішно обчислено.',
    'summary' => [
        'totalClients'            => $totalClients,
        'highProbabilityClients'  => $highCount,
        'averageProbability'      => round($avgProb, 3)
    ],
    'data' => $result
], JSON_UNESCAPED_UNICODE);
