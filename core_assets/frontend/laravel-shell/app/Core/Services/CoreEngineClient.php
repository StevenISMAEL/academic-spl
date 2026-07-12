<?php

namespace App\Core\Services;

use Illuminate\Support\Facades\Http;
use Exception;

/**
 * Core Asset — CoreEngineClient (COR-17)
 *
 * Cliente HTTP unificado para comunicarse con el Core Engine (FastAPI).
 * Define políticas de timeout de 3s y propaga errores HTTP de forma clara.
 */
class CoreEngineClient
{
    private string $baseUrl;
    private int $timeout = 3;

    public function __construct()
    {
        $this->baseUrl = rtrim(config('core_engine.backend_url', 'http://127.0.0.1:8001'), '/');
    }

    /**
     * Realiza una petición GET.
     */
    public function get(string $endpoint, array $query = []): array
    {
        return $this->request('GET', $endpoint, ['query' => $query]);
    }

    /**
     * Realiza una petición POST.
     */
    public function post(string $endpoint, array $data = []): array
    {
        return $this->request('POST', $endpoint, ['json' => $data]);
    }

    /**
     * Realiza una petición PUT.
     */
    public function put(string $endpoint, array $data = []): array
    {
        return $this->request('PUT', $endpoint, ['json' => $data]);
    }

    /**
     * Realiza una petición PATCH.
     */
    public function patch(string $endpoint, array $data = []): array
    {
        return $this->request('PATCH', $endpoint, ['json' => $data]);
    }

    /**
     * Realiza una petición DELETE.
     */
    public function delete(string $endpoint): array
    {
        return $this->request('DELETE', $endpoint);
    }

    /**
     * Envía la petición HTTP encapsulando la lógica común.
     */
    private function request(string $method, string $endpoint, array $options = []): array
    {
        $url = $this->baseUrl . '/' . ltrim($endpoint, '/');
        $request = Http::timeout($this->timeout);

        if (isset($options['query'])) {
            $request = $request->withQueryParameters($options['query']);
        }

        $response = match ($method) {
            'GET' => $request->get($url),
            'POST' => $request->post($url, $options['json'] ?? []),
            'PUT' => $request->put($url, $options['json'] ?? []),
            'PATCH' => $request->patch($url, $options['json'] ?? []),
            'DELETE' => $request->delete($url),
            default => throw new Exception("Método HTTP no soportado: {$method}"),
        };

        if ($response->failed()) {
            $this->handleErrorResponse($response);
        }

        return $response->json() ?? [];
    }

    /**
     * Procesa la respuesta de error del backend y lanza una excepción clara.
     */
    private function handleErrorResponse($response): void
    {
        $status = $response->status();
        $body = $response->json();

        // Extrae el mensaje de error del backend si existe (FastAPI suele devolver {"detail": "..."})
        $message = null;
        if (is_array($body) && isset($body['detail'])) {
            if (is_array($body['detail'])) {
                // Errores de validación de FastAPI (Pydantic ValidationError)
                $errors = [];
                foreach ($body['detail'] as $err) {
                    $loc = implode('.', $err['loc'] ?? []);
                    $msg = $err['msg'] ?? 'Error de validación';
                    $errors[] = "{$loc}: {$msg}";
                }
                $message = implode(' | ', $errors);
            } else {
                $message = $body['detail'];
            }
        }

        $errorMessage = $message ?: "Error HTTP {$status}: " . ($response->reason() ?: 'Respuesta fallida');
        throw new Exception($errorMessage, $status);
    }
}
