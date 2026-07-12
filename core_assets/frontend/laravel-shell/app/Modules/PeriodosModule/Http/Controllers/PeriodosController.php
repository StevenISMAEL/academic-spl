<?php

namespace App\Modules\PeriodosModule\Http\Controllers;

use App\Core\Services\CoreEngineClient;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Exception;

class PeriodosController extends Controller
{
    protected CoreEngineClient $client;

    public function __construct()
    {
        $this->client = new CoreEngineClient();
    }

    public function index()
    {
        $response = $this->client->get('/periodos/');
        $periodos = $response['data'] ?? [];

        return view('periodos.index', compact('periodos'));
    }

    public function store(Request $request)
    {
        $request->validate([
            'id' => 'required|string',
            'nombre' => 'required|string',
            'fecha_inicio' => 'required|date',
            'fecha_fin' => 'required|date',
        ]);

        try {
            $this->client->post('/periodos/', $request->only(['id', 'nombre', 'fecha_inicio', 'fecha_fin']));
            return redirect('/periodos')->with('success', 'Período académico registrado correctamente.');
        } catch (Exception $e) {
            return back()->withInput()->withErrors(['error' => $e->getMessage()]);
        }
    }
}
