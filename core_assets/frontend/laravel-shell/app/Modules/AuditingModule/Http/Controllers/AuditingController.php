<?php

namespace App\Modules\AuditingModule\Http\Controllers;

use App\Core\Services\CoreEngineClient;
use App\Core\Services\FeatureGate;
use App\Http\Controllers\Controller;
use Symfony\Component\HttpFoundation\Response;

class AuditingController extends Controller
{
    protected CoreEngineClient $client;

    public function __construct()
    {
        $this->client = new CoreEngineClient();
    }

    public function index()
    {
        abort_unless(FeatureGate::isActive('auditing'), Response::HTTP_NOT_FOUND);

        $response = $this->client->get('/auditing/');
        
        // El endpoint devuelve una lista directa o un diccionario?
        // En router.py dice: return repo.get_logs(limit, offset) 
        // Y get_logs devuelve una List[Dict] (un array de objetos).
        // En caso de que haya wrap o no, lo manejamos.
        $registros = is_array($response) && isset($response['data']) ? $response['data'] : $response;

        return view('modules.auditing.index', compact('registros'));
    }
}
