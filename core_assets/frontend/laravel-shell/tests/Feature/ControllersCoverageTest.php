<?php

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Http;
use Tests\TestCase;

class ControllersCoverageTest extends TestCase
{
    use RefreshDatabase;

    protected function setUp(): void
    {
        parent::setUp();
        config(['core_engine.backend_url' => 'http://127.0.0.1:8001']);
        Cache::flush();
    }

    public function test_attendance_index_renders_view_with_backend_data(): void
    {
        Http::fake([
            'http://127.0.0.1:8001/' => Http::response([
                'product' => 'colegio-basico',
                'active_optional_features' => ['attendance'],
                'academic_settings' => [],
            ], 200),
            'http://127.0.0.1:8001/attendance/' => Http::response([
                'estadisticas' => [
                    'porcentaje_asistencia' => 90,
                    'estado' => 'APROBADO',
                    'total_presentes' => 18,
                    'total_ausentes' => 2,
                    'umbral_aprobado' => 80,
                    'umbral_riesgo' => 70,
                    'total_registros' => 20,
                ],
                'resumen_por_persona' => [
                    ['persona_id' => 'P-001', 'total' => 2, 'presentes' => 2, 'porcentaje' => 100, 'estado' => 'APROBADO'],
                ],
                'data' => [
                    ['persona_id' => 'P-001', 'curso_id' => 'C-001', 'fecha' => '2026-01-10', 'presente' => true, 'justificacion' => ''],
                ],
            ], 200),
            'http://127.0.0.1:8001/personas/' => Http::response(['data' => [['id' => 'P-001']]], 200),
            'http://127.0.0.1:8001/cursos/' => Http::response(['data' => [['id' => 'C-001']]], 200),
        ]);

        $user = new User([
            'name' => 'Test User',
            'email' => 'test@example.com',
            'password' => bcrypt('secret'),
        ]);

        $response = $this->actingAs($user)->get('/attendance');

        $response->assertOk();
        $response->assertViewIs('modules.attendance.index');
        $response->assertViewHas('estadisticas');
        $response->assertViewHas('registros');
        $response->assertViewHas('personas');
        $response->assertViewHas('cursos');
    }

    public function test_attendance_store_redirects_with_success_message(): void
    {
        Http::fake([
            'http://127.0.0.1:8001/' => Http::response([
                'product' => 'colegio-basico',
                'active_optional_features' => ['attendance'],
                'academic_settings' => [],
            ], 200),
            'http://127.0.0.1:8001/attendance/' => Http::response(['ok' => true], 200),
        ]);

        $user = new User([
            'name' => 'Test User',
            'email' => 'test@example.com',
            'password' => bcrypt('secret'),
        ]);

        $response = $this->actingAs($user)->post('/attendance', [
            'persona_id' => 'P-001',
            'curso_id' => 'C-001',
            'fecha' => '2026-01-10',
            'presente' => true,
            'justificacion' => 'Sin novedad',
        ]);

        $response->assertRedirect('/attendance');
        $response->assertSessionHas('success', 'Registro de asistencia guardado.');
    }

    public function test_attendance_store_returns_back_on_validation_or_server_error(): void
    {
        Http::fake([
            'http://127.0.0.1:8001/' => Http::response([
                'product' => 'colegio-basico',
                'active_optional_features' => ['attendance'],
                'academic_settings' => [],
            ], 200),
            'http://127.0.0.1:8001/attendance/' => Http::response(['detail' => 'error'], 500),
        ]);

        $user = new User([
            'name' => 'Test User',
            'email' => 'test@example.com',
            'password' => bcrypt('secret'),
        ]);

        $response = $this->actingAs($user)->from('/attendance')->post('/attendance', [
            'persona_id' => 'P-001',
            'curso_id' => 'C-001',
            'fecha' => '2026-01-10',
            'presente' => 'no-es-boolean',
        ]);

        $response->assertRedirect('/attendance');
        $response->assertSessionHasErrors(['presente']);
    }

    public function test_auditing_index_renders_registros_from_backend(): void
    {
        Http::fake([
            'http://127.0.0.1:8001/' => Http::response([
                'product' => 'colegio-basico',
                'active_optional_features' => ['auditing'],
                'academic_settings' => [],
            ], 200),
            'http://127.0.0.1:8001/auditing/' => Http::response([
                ['id' => 'A-1', 'accion' => 'login'],
                ['id' => 'A-2', 'accion' => 'logout'],
            ], 200),
        ]);

        $user = new User([
            'name' => 'Test User',
            'email' => 'test@example.com',
            'password' => bcrypt('secret'),
        ]);

        $response = $this->actingAs($user)->get('/auditing');

        $response->assertOk();
        $response->assertViewIs('modules.auditing.index');
        $response->assertViewHas('registros');
    }

    public function test_certificates_index_and_by_persona_and_generate(): void
    {
        Http::fake([
            'http://127.0.0.1:8001/' => Http::response([
                'product' => 'colegio-basico',
                'active_optional_features' => ['certificates'],
                'academic_settings' => [],
            ], 200),
            'http://127.0.0.1:8001/certificates/' => Http::response(['data' => [['id' => 'CERT-1']]], 200),
            'http://127.0.0.1:8001/certificates/persona/P-001' => Http::response(['data' => [['id' => 'CERT-1']]], 200),
            'http://127.0.0.1:8001/personas/' => Http::response(['data' => [['id' => 'P-001']]], 200),
            'http://127.0.0.1:8001/certificates/P-001/generate' => Http::response([
                'certificado' => ['estado' => 'emitido'],
            ], 200),
        ]);

        $user = new User([
            'name' => 'Test User',
            'email' => 'test@example.com',
            'password' => bcrypt('secret'),
        ]);

        $this->actingAs($user)->get('/certificates')->assertOk()->assertViewIs('certificates.index');
        $this->actingAs($user)->get('/certificates/persona/P-001')->assertOk()->assertViewIs('certificates.index');

        $response = $this->actingAs($user)->post('/certificates/P-001/generate');
        $response->assertRedirect(route('certificates.index'));
        $response->assertSessionHas('success', '✅ Certificado emitido exitosamente.');
    }

    public function test_certificates_generate_rejected_status_sets_error_session(): void
    {
        Http::fake([
            'http://127.0.0.1:8001/' => Http::response([
                'product' => 'colegio-basico',
                'active_optional_features' => ['certificates'],
                'academic_settings' => [],
            ], 200),
            'http://127.0.0.1:8001/certificates/' => Http::response(['data' => [['id' => 'CERT-1']]], 200),
            'http://127.0.0.1:8001/personas/' => Http::response(['data' => [['id' => 'P-001']]], 200),
            'http://127.0.0.1:8001/certificates/P-001/generate' => Http::response([
                'certificado' => [
                    'estado' => 'rechazado',
                    'motivo_rechazo' => 'Falta asistencia mínima',
                ],
            ], 200),
        ]);

        $user = new User([
            'name' => 'Test User',
            'email' => 'cert-reject@example.com',
            'password' => bcrypt('secret'),
        ]);

        $this->actingAs($user)
            ->from('/certificates')
            ->post('/certificates/P-001/generate')
            ->assertRedirect(route('certificates.index'))
            ->assertSessionHas('error', '⚠️ Certificado rechazado: Falta asistencia mínima');
    }

    public function test_cursos_index_and_store(): void
    {
        Http::fake([
            'http://127.0.0.1:8001/' => Http::response([
                'product' => 'colegio-basico',
                'active_optional_features' => ['attendance'],
                'academic_settings' => [],
            ], 200),
            'http://127.0.0.1:8001/cursos/' => Http::response(['data' => [['id' => 'C-001']]], 200),
            'http://127.0.0.1:8001/periodos/' => Http::response(['data' => [['id' => 'PER-001']]], 200),
        ]);

        $user = new User([
            'name' => 'Test User',
            'email' => 'test@example.com',
            'password' => bcrypt('secret'),
        ]);

        $this->actingAs($user)->get('/cursos')->assertOk()->assertViewIs('cursos.index');

        $response = $this->actingAs($user)->post('/cursos', [
            'id' => 'C-002',
            'nombre' => 'Física',
            'periodo_id' => 'PER-001',
        ]);

        $response->assertRedirect('/cursos');
        $response->assertSessionHas('success', 'Curso registrado correctamente.');
    }

    public function test_schedule_index_store_and_destroy_flow(): void
    {
        Http::fake(function ($request) {
            if ($request->url() === 'http://127.0.0.1:8001/' && $request->method() === 'GET') {
                return Http::response([
                    'product' => 'colegio-basico',
                    'active_optional_features' => ['schedule'],
                    'academic_settings' => [],
                ], 200);
            }

            if ($request->url() === 'http://127.0.0.1:8001/schedule/' && $request->method() === 'GET') {
                return Http::response([
                    'horarios' => [[
                        'id' => 'S-001',
                        'curso_id' => 'C-001',
                        'nombre_curso' => 'Matemática',
                        'dia_semana' => 'Lunes',
                        'hora_inicio' => '08:00',
                        'hora_fin' => '10:00',
                        'aula' => 'A-101',
                    ]],
                    'horarios_por_dia' => [
                        'Lunes' => [[
                            'id' => 'S-001',
                            'curso_id' => 'C-001',
                            'nombre_curso' => 'Matemática',
                            'dia_semana' => 'Lunes',
                            'hora_inicio' => '08:00',
                            'hora_fin' => '10:00',
                            'aula' => 'A-101',
                        ]],
                    ],
                    'periods_per_year' => 2,
                    'product_name' => 'colegio-basico',
                    'dias_validos' => ['Lunes', 'Martes'],
                ], 200);
            }

            if ($request->url() === 'http://127.0.0.1:8001/cursos/' && $request->method() === 'GET') {
                return Http::response([
                    'data' => [['id' => 'C-001', 'nombre' => 'Matemática']],
                ], 200);
            }

            if ($request->url() === 'http://127.0.0.1:8001/schedule/' && $request->method() === 'POST') {
                return Http::response(['ok' => true], 200);
            }

            if ($request->url() === 'http://127.0.0.1:8001/schedule/S-001' && $request->method() === 'DELETE') {
                return Http::response(['ok' => true], 200);
            }

            return Http::response(['ok' => true], 200);
        });

        $user = new User([
            'name' => 'Schedule User',
            'email' => 'schedule@example.com',
            'password' => bcrypt('secret'),
        ]);

        $this->actingAs($user)->get('/schedule')->assertOk()->assertViewIs('schedule.index')->assertViewHas('data')->assertViewHas('cursos');

        $this->actingAs($user)->from('/schedule')->post('/schedule', [
            'curso_id' => 'C-001',
            'dia_semana' => 'Lunes',
            'hora_inicio' => '08:00',
            'hora_fin' => '10:00',
            'aula' => 'A-101',
        ])->assertRedirect(route('schedule.index'))->assertSessionHas('success', '✅ Horario creado exitosamente.');

        $this->actingAs($user)->delete('/schedule/S-001')->assertRedirect(route('schedule.index'))->assertSessionHas('success', '✅ Horario eliminado.');
    }

    public function test_schedule_is_blocked_when_feature_gate_is_inactive(): void
    {
        Http::fake([
            'http://127.0.0.1:8001/' => Http::response([
                'product' => 'colegio-basico',
                'active_optional_features' => [],
                'academic_settings' => [],
            ], 200),
        ]);

        $user = new User([
            'name' => 'Schedule User',
            'email' => 'schedule-off@example.com',
            'password' => bcrypt('secret'),
        ]);

        $this->actingAs($user)->get('/schedule')->assertNotFound();
    }

    public function test_enrollment_index_store_update_and_destroy(): void
    {
        Http::fake([
            'http://127.0.0.1:8001/' => Http::response([
                'product' => 'colegio-basico',
                'active_optional_features' => ['enrollment'],
                'academic_settings' => [],
            ], 200),
            'http://127.0.0.1:8001/enrollment/' => Http::response(['data' => [['id' => 'M-001']]], 200),
            'http://127.0.0.1:8001/personas/' => Http::response(['data' => [['id' => 'P-001']]], 200),
            'http://127.0.0.1:8001/cursos/' => Http::response(['data' => [['id' => 'C-001']]], 200),
            'http://127.0.0.1:8001/enrollment/' => Http::response(['ok' => true], 200),
            'http://127.0.0.1:8001/enrollment/M-001/status' => Http::response(['ok' => true], 200),
            'http://127.0.0.1:8001/enrollment/M-001' => Http::response(['ok' => true], 200),
        ]);

        $user = new User([
            'name' => 'Test User',
            'email' => 'test@example.com',
            'password' => bcrypt('secret'),
        ]);

        $this->actingAs($user)->get('/enrollment')->assertOk()->assertViewIs('enrollment.index');

        $this->actingAs($user)->post('/enrollment', [
            'persona_id' => 'P-001',
            'curso_id' => 'C-001',
        ])->assertRedirect('/enrollment')->assertSessionHas('success', 'Matrícula registrada correctamente.');

        $this->actingAs($user)->patch('/enrollment/M-001/status', [
            'estado' => 'aprobado',
        ])->assertRedirect('/enrollment')->assertSessionHas('success', 'Estado de matrícula actualizado.');

        $this->actingAs($user)->delete('/enrollment/M-001')->assertRedirect('/enrollment')->assertSessionHas('success', 'Matrícula eliminada correctamente.');
    }

    public function test_enrollment_store_returns_validation_error_when_request_is_invalid(): void
    {
        Http::fake([
            'http://127.0.0.1:8001/' => Http::response([
                'product' => 'colegio-basico',
                'active_optional_features' => ['enrollment'],
                'academic_settings' => [],
            ], 200),
        ]);

        $user = new User([
            'name' => 'Test User',
            'email' => 'test@example.com',
            'password' => bcrypt('secret'),
        ]);

        $this->actingAs($user)->from('/enrollment')->post('/enrollment', [
            'persona_id' => '',
            'curso_id' => '',
        ])->assertSessionHasErrors(['persona_id', 'curso_id']);
    }

    public function test_enrollment_index_is_blocked_when_feature_gate_is_inactive(): void
    {
        Http::fake([
            'http://127.0.0.1:8001/' => Http::response([
                'product' => 'colegio-basico',
                'active_optional_features' => [],
                'academic_settings' => [],
            ], 200),
        ]);

        $user = new User([
            'name' => 'Test User',
            'email' => 'test@example.com',
            'password' => bcrypt('secret'),
        ]);

        $this->actingAs($user)->get('/enrollment')->assertNotFound();
    }
}
