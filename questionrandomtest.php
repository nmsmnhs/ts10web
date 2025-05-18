<?php
ini_set('display_errors', 1);
error_reporting(E_ALL);

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

$host = "sql102.infinityfree.com";
$user = "if0_38953247";
$password = "rwcG0UxaUUD";
$dbname = "if0_38953247_dbEngTest";

$conn = new mysqli($host, $user, $password, $dbname);

if ($conn->connect_error) {
    echo json_encode(["error" => "Connection failed: " . $conn->connect_error]);
    exit;
}

$conn->set_charset("utf8mb4");

// Get question type from GET or POST
$type = isset($_GET['type']) ? $_GET['type'] : '';
$allowed_types = ['dbVocabulary', 'dbGrammar', 'dbPhonetics', 'dbStress', 'dbSentenceTransformation', 'dbGuidedCloze', 'dbRearrangement', 'dbReading', 'dbWordform']; // Add all allowed table names


$type_map = [
    'Phonetics' => 'dbPhonetics',
    'Stress' => 'dbStress',
    'Sentence_transformation' => 'dbSentenceTransformation', // match HTML value and actual table name
    'Vocabulary' => 'dbVocabulary',
    'Grammar' => 'dbGrammar',
    'GuidedCloze' => 'dbGuidedCloze',
    'Rearrangement' => 'dbRearrangement',
    'Reading' => 'dbReading',
    'Wordform' => 'dbWordform'

];

$table = isset($type_map[$type]) ? $type_map[$type] : '';

if (!$table || !in_array($table, $allowed_types)) {
    echo json_encode(["error" => "Invalid question type."]);
    exit;
}

$sql = "
SELECT 
    COL2 AS Question, 
    COL3 AS Answer, 
    COL4 AS Explanation 
FROM 
    $table
WHERE 
    id > (SELECT MIN(id) FROM $table)
ORDER BY 
    RAND() 
LIMIT 
    1";
$result = $conn->query($sql);

if ($result && $result->num_rows > 0) {
    $row = $result->fetch_assoc();
    $question = nl2br(htmlspecialchars($row['Question']));
    $answer = htmlspecialchars($row['Answer']);
    $explanation = nl2br(htmlspecialchars($row['Explanation']));
    echo json_encode([
        "Question" => $question,
        "Answer" => $answer,
        "Explanation" => $explanation
    ]);
} else {
    echo json_encode(["error" => "No questions found in the database."]);
}

$conn->close();
?>