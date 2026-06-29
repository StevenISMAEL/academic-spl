<?php

namespace App\Modules\AttendanceModule\Http\Controllers;

use App\Core\Services\FeatureGate;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

/**
 * Core Asset (plantilla) — Módulo Attendance, ejemplo de patrón
 * desacoplado (COR-10).
 *
 * Este controlador es la plantilla que cualquier futuro módulo debe
 * seguir: 1) se autoverifica activo antes de hacer nada, 2) vive
 * completamente fuera de app/Http/Controllers central, 3) no depende
 * de ningún otro módulo.
 */
class AttendanceController extends Controller
{
    public function index()
    {
        // Defensa en profundidad: aunque la ruta esté registrada, el
        // propio módulo se niega a responder si no está activo. Así,
        // ni un error de configuración en las rutas expone el módulo.
        abort_unless(FeatureGate::isActive('attendance'), Response::HTTP_NOT_FOUND);

        $sampleData = [
            ['persona' => 'P-001', 'curso' => 'C-001', 'presente' => true],
            ['persona' => 'P-002', 'curso' => 'C-001', 'presente' => false],
        ];

        return view('modules.attendance.index', ['registros' => $sampleData]);
    }
}
