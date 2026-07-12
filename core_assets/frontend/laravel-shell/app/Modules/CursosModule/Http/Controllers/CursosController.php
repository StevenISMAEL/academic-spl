<?php

namespace App\Modules\CursosModule\Http\Controllers;

use App\Core\Services\CoreEngineClient;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Exception;

class CursosController extends Controller
{
    protected CoreEngineClient $client;

    public function __construct()
    {
        $this->client = new CoreEngineClient();
    }

    public function index()
    {
        $cursosResponse = $this->client->get('/cursos/');
        $periodosResponse = $this->client->get('/periodos/');

        $cursos = $cursosResponse['data'] ?? [];
        $periodos = $periodosResponse['data'] ?? [];

        return view('cursos.index', compact('cursos', 'periodos'));
    }

    public function store(Request $request)
    {
        $request->validate([
            'id' => 'required|string',
            'nombre' => 'required|string',
            'periodo_id' => 'required|string',
        ]);

        try {
            $this->client->post('/cursos/', $request->only(['id', 'nombre', 'periodo_id']));
            return redirect('/cursos')->with('success', 'Curso registrado correctamente.');
        } catch (Exception $e) {
            return back()->withInput()->withErrors(['error' => $e->getMessage()]);
        }
    }
}
