<?php

namespace App\Modules\GradingModule\Http\Controllers;

use App\Core\Services\CoreEngineClient;
use App\Core\Services\FeatureGate;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Exception;

class GradingController extends Controller
{
    protected CoreEngineClient $client;

    public function __construct()
    {
        $this->client = new CoreEngineClient();
    }

    public function index()
    {
        abort_unless(FeatureGate::isActive('grading'), 404);

        $response = $this->client->get('/grading/');
        $notas = $response['data'] ?? [];
        $scale = $response['evaluation_scale_used'] ?? 'N/A';
        $passing = $response['passing_grade_used'] ?? 'N/A';

        $personasResponse = $this->client->get('/personas/');
        $cursosResponse = $this->client->get('/cursos/');

        $personas = $personasResponse['data'] ?? [];
        $cursos = $cursosResponse['data'] ?? [];

        return view('grading.index', compact('notas', 'scale', 'passing', 'personas', 'cursos'));
    }

    public function store(Request $request)
    {
        abort_unless(FeatureGate::isActive('grading'), 404);

        $request->validate([
            'persona_id' => 'required|string',
            'curso_id' => 'required|string',
            'valor' => 'required|numeric|min:0|max:10',
        ]);

        try {
            $this->client->post('/grading/', $request->only(['persona_id', 'curso_id', 'valor', 'observacion']));
            return redirect('/grading')->with('success', 'Calificación registrada correctamente.');
        } catch (Exception $e) {
            return back()->withInput()->withErrors(['error' => $e->getMessage()]);
        }
    }

    public function destroy(string $id)
    {
        abort_unless(FeatureGate::isActive('grading'), 404);

        try {
            $this->client->delete("/grading/{$id}");
            return redirect('/grading')->with('success', 'Calificación eliminada correctamente.');
        } catch (Exception $e) {
            return back()->withErrors(['error' => $e->getMessage()]);
        }
    }
}
