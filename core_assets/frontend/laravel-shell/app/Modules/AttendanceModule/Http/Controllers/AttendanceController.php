<?php

namespace App\Modules\AttendanceModule\Http\Controllers;

use App\Core\Services\CoreEngineClient;
use App\Core\Services\FeatureGate;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Exception;
use Symfony\Component\HttpFoundation\Response;

/**
 * Core Asset (refactorizado) — Módulo Attendance Sprint 2.
 * Reemplaza los datos hardcodeados por llamadas reales al Core Engine.
 * Muestra estadísticas CA-03 (AttendanceCalculator) y resumen por persona.
 */
class AttendanceController extends Controller
{
    protected CoreEngineClient $client;

    public function __construct()
    {
        $this->client = new CoreEngineClient();
    }

    public function index()
    {
        abort_unless(FeatureGate::isActive('attendance'), Response::HTTP_NOT_FOUND);

        $response = $this->client->get('/attendance/');

        $estadisticas = $response['estadisticas'] ?? [];
        $resumen      = $response['resumen_por_persona'] ?? [];
        $registros    = $response['data'] ?? [];

        $personasResponse = $this->client->get('/personas/');
        $cursosResponse = $this->client->get('/cursos/');

        $personas = $personasResponse['data'] ?? [];
        $cursos = $cursosResponse['data'] ?? [];

        return view('modules.attendance.index', compact('estadisticas', 'resumen', 'registros', 'personas', 'cursos'));
    }

    public function store(Request $request)
    {
        abort_unless(FeatureGate::isActive('attendance'), Response::HTTP_NOT_FOUND);

        $request->validate([
            'persona_id' => 'required|string',
            'curso_id'   => 'required|string',
            'fecha'      => 'required|date',
            'presente'   => 'boolean',
        ]);

        try {
            $data = $request->only(['persona_id', 'curso_id', 'fecha']);
            $data['presente'] = $request->boolean('presente');
            $data['justificacion'] = $request->input('justificacion');
            $this->client->post('/attendance/', $data);
            return redirect('/attendance')->with('success', 'Registro de asistencia guardado.');
        } catch (Exception $e) {
            return back()->withInput()->withErrors(['error' => $e->getMessage()]);
        }
    }
}
