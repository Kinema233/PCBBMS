<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

$action = $_GET['action'] ?? '';

function initJsonFile($filename) {
    if (!file_exists($filename)) {
        file_put_contents($filename, json_encode([]));
    }
}

initJsonFile('vehicles.json');
initJsonFile('reports.json');

switch ($action) {
    case 'getVehicles':
        $vehicles = json_decode(file_get_contents('vehicles.json'), true);
        echo json_encode($vehicles);
        break;
        
    case 'addVehicle':
        $data = json_decode(file_get_contents('php://input'), true);
        $vehicles = json_decode(file_get_contents('vehicles.json'), true);
        
        $newVehicle = [
            'id' => uniqid(),
            'brand' => htmlspecialchars($data['brand']),
            'model' => htmlspecialchars($data['model']),
            'year' => intval($data['year']),
            'plate' => htmlspecialchars($data['plate']),
            'status' => $data['status']
        ];
        
        $vehicles[] = $newVehicle;
        file_put_contents('vehicles.json', json_encode($vehicles, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
        
        echo json_encode(['success' => true, 'message' => 'Транспорт додано']);
        break;
        
    case 'deleteVehicle':
        $id = $_GET['id'] ?? '';
        $vehicles = json_decode(file_get_contents('vehicles.json'), true);
        
        $filtered = array_filter($vehicles, function($v) use ($id) {
            return $v['id'] !== $id;
        });
        
        file_put_contents('vehicles.json', json_encode(array_values($filtered), JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
        echo json_encode(['success' => true]);
        break;
        
    case 'getReports':
        $reports = json_decode(file_get_contents('reports.json'), true);
        echo json_encode($reports);
        break;
        
    case 'addReport':
        $data = json_decode(file_get_contents('php://input'), true);
        $reports = json_decode(file_get_contents('reports.json'), true);
        
        $newReport = [
            'id' => uniqid(),
            'vehicle_id' => $data['vehicle_id'],
            'date' => $data['date'],
            'inspector' => htmlspecialchars($data['inspector']),
            'condition' => $data['condition'],
            'notes' => htmlspecialchars($data['notes'])
        ];
        
        $reports[] = $newReport;
        file_put_contents('reports.json', json_encode($reports, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
        
        echo json_encode(['success' => true, 'message' => 'Звіт додано']);
        break;
        
    default:
        echo json_encode(['error' => 'Невідома дія']);
        break;
}
?>