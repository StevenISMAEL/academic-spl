<?php

namespace App\Modules\ScheduleModule\Http\Controllers;

use App\Core\Services\CoreEngineClient;
use App\Core\Services\FeatureGate;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class ScheduleController extends Controller
{
    public function index()
    {
        abort_unless(FeatureGate::isActive('schedule'), 404);

        $client  = new CoreEngineClient();
        $data    = $client->get('/schedule/');

        // /cursos/ devuelve {"service":"cursos","data":[...]}
        $cursosData = $client->get('/cursos/');
        $cursos     = $cursosData['data'] ?? [];

        return view('schedule.index', compact('data', 'cursos'));
    }

    public function store(Request $request)
    {
        abort_unless(FeatureGate::isActive('schedule'), 404);

        $client = new CoreEngineClient();
        $client->post('/schedule/', [
            'curso_id'    => $request->input('curso_id'),
            'dia_semana'  => $request->input('dia_semana'),
            'hora_inicio' => $request->input('hora_inicio'),
            'hora_fin'    => $request->input('hora_fin'),
            'aula'        => $request->input('aula'),
        ]);

        return redirect()->route('schedule.index')->with('success', '✅ Horario creado exitosamente.');
    }

    public function destroy(string $scheduleId)
    {
        abort_unless(FeatureGate::isActive('schedule'), 404);

        $client = new CoreEngineClient();
        $client->delete("/schedule/{$scheduleId}");

        return redirect()->route('schedule.index')->with('success', '✅ Horario eliminado.');
    }
}
