<!DOCTYPE html>
<html>
<head><title>Grading</title></head>
<body>
    <h1>Grading</h1>
    <p>Notas: {{ json_encode($notas) }}</p>
    <p>Escala: {{ $scale }}</p>
    <p>Aprobación: {{ $passing }}</p>
</body>
</html>
