<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Academic SPL</title>
    <!-- Add some basic styling so it looks decent -->
    <style>
        body {
            font-family: system-ui, -apple-system, sans-serif;
            background-color: #f3f4f6;
            color: #1f2937;
            margin: 0;
            padding: 2rem;
            display: flex;
            justify-content: center;
        }
        .container {
            background-color: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            width: 100%;
            max-width: 800px;
        }
        input {
            border: 1px solid #d1d5db;
            border-radius: 4px;
        }
        button {
            background-color: #2563eb;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #1d4ed8;
        }
    </style>
</head>
<body>
    <div class="container">
        {{ $slot }}
    </div>
</body>
</html>
