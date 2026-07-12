<?php

namespace App\Modules\PersonasModule\Http\Controllers;

use App\Core\Services\CoreEngineClient;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Exception;

class PersonasController extends Controller
{
    protected CoreEngineClient $client;

    public function __construct()
    {
        $this->client = new CoreEngineClient();
    }

    public function index()
    {
        $response = $this->client->get('/personas/');
        $personas = $response['data'] ?? [];

        return view('personas.index', compact('personas'));
    }

    public function store(Request $request)
    {
        $request->validate([
            'nombres' => 'required|string',
            'apellidos' => 'required|string',
            'documento_identidad' => 'required|string',
        ]);

        try {
            $this->client->post('/personas/', $request->only(['nombres', 'apellidos', 'documento_identidad']));
            return redirect('/personas')->with('success', 'Persona registrada correctamente.');
        } catch (Exception $e) {
            // FastAPI validation or key constraint error is caught and returned (e.g. invalid identification document)
            return back()->withInput()->withErrors(['error' => $e->getMessage()]);
        }
    }
}
