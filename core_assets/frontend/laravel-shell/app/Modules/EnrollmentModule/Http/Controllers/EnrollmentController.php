<?php

namespace App\Modules\EnrollmentModule\Http\Controllers;

use App\Core\Services\CoreEngineClient;
use App\Core\Services\FeatureGate;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Exception;

class EnrollmentController extends Controller
{
    protected CoreEngineClient $client;

    public function __construct()
    {
        $this->client = new CoreEngineClient();
    }

    public function index()
    {
        abort_unless(FeatureGate::isActive('enrollment'), 404);

        $response = $this->client->get('/enrollment/');
        $matriculas = $response['data'] ?? [];

        $personasResponse = $this->client->get('/personas/');
        $cursosResponse = $this->client->get('/cursos/');

        $personas = $personasResponse['data'] ?? [];
        $cursos = $cursosResponse['data'] ?? [];

        return view('enrollment.index', compact('matriculas', 'personas', 'cursos'));
    }

    public function store(Request $request)
    {
        abort_unless(FeatureGate::isActive('enrollment'), 404);

        $request->validate([
            'persona_id' => 'required|string',
            'curso_id'   => 'required|string',
        ]);

        try {
            $this->client->post('/enrollment/', $request->only(['persona_id', 'curso_id']));
            return redirect('/enrollment')->with('success', 'Matrícula registrada correctamente.');
        } catch (Exception $e) {
            // HTTP 409 = límite de materias superado (CA-05)
            return back()->withInput()->withErrors(['limite' => $e->getMessage()]);
        }
    }

    public function updateStatus(Request $request, string $id)
    {
        abort_unless(FeatureGate::isActive('enrollment'), 404);

        $request->validate([
            'estado' => 'required|in:inscrito,retirado,aprobado,reprobado',
        ]);

        try {
            $this->client->patch("/enrollment/{$id}/status", ['estado' => $request->input('estado')]);
            return redirect('/enrollment')->with('success', 'Estado de matrícula actualizado.');
        } catch (Exception $e) {
            return back()->withErrors(['error' => $e->getMessage()]);
        }
    }

    public function destroy(string $id)
    {
        abort_unless(FeatureGate::isActive('enrollment'), 404);

        try {
            $this->client->delete("/enrollment/{$id}");
            return redirect('/enrollment')->with('success', 'Matrícula eliminada correctamente.');
        } catch (Exception $e) {
            return back()->withErrors(['error' => $e->getMessage()]);
        }
    }
}
