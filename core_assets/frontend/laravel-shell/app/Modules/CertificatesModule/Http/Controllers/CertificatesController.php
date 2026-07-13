<?php

namespace App\Modules\CertificatesModule\Http\Controllers;

use App\Core\Services\CoreEngineClient;
use App\Core\Services\FeatureGate;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class CertificatesController extends Controller
{
    public function index()
    {
        abort_unless(FeatureGate::isActive('certificates'), 404);

        $client = new CoreEngineClient();
        $data   = $client->get('/certificates/');

        // /personas/ devuelve {"service":"personas","data":[...]}
        $personasData = $client->get('/personas/');
        $personas     = $personasData['data'] ?? [];

        return view('certificates.index', compact('data', 'personas'));
    }

    public function byPersona(string $personaId)
    {
        abort_unless(FeatureGate::isActive('certificates'), 404);

        $client = new CoreEngineClient();
        $data   = $client->get("/certificates/persona/{$personaId}");

        // /personas/ devuelve {"service":"personas","data":[...]}
        $personasData = $client->get('/personas/');
        $personas     = $personasData['data'] ?? [];

        return view('certificates.index', compact('data', 'personas'));
    }

    public function generate(Request $request, string $personaId)
    {
        abort_unless(FeatureGate::isActive('certificates'), 404);

        $client = new CoreEngineClient();
        $result = $client->post("/certificates/{$personaId}/generate", []);

        $estado  = $result['certificado']['estado'] ?? 'desconocido';
        $message = $estado === 'emitido'
            ? '✅ Certificado emitido exitosamente.'
            : '⚠️ Certificado rechazado: ' . ($result['certificado']['motivo_rechazo'] ?? 'Requisitos no cumplidos.');

        $sessionKey = $estado === 'emitido' ? 'success' : 'error';
        return redirect()->route('certificates.index')->with($sessionKey, $message);
    }
}
