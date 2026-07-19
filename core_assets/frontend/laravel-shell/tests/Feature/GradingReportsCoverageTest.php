<?php

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Http;
use Tests\TestCase;

class GradingReportsCoverageTest extends TestCase
{
    use RefreshDatabase;

    protected function setUp(): void
    {
        parent::setUp();
        config(['core_engine.backend_url' => 'http://127.0.0.1:8001']);
        Cache::flush();
    }

    public function test_grading_index_and_store_and_destroy_flow(): void
    {
        Http::fake([
            'http://127.0.0.1:8001/' => Http::response([
                'product' => 'colegio-basico',
                'active_optional_features' => ['grading'],
                'academic_settings' => [],
            ], 200),
            'http://127.0.0.1:8001/grading/' => Http::response([
                'data' => [['id' => 'G-001', 'persona_id' => 'P-001', 'curso_id' => 'C-001', 'valor' => 8.5]],
                'evaluation_scale_used' => 'literal',
                'passing_grade_used' => 7.0,
            ], 200),
            'http://127.0.0.1:8001/grading/G-001' => Http::response(['ok' => true], 200),
            'http://127.0.0.1:8001/personas/' => Http::response(['data' => [['id' => 'P-001']]], 200),
            'http://127.0.0.1:8001/cursos/' => Http::response(['data' => [['id' => 'C-001']]], 200),
        ]);

        $user = User::create([
            'name' => 'Test User',
            'email' => 'grading@example.com',
            'password' => bcrypt('secret123'),
        ]);

        $this->actingAs($user)->get('/grading')->assertOk()->assertViewIs('grading.index');

        $this->actingAs($user)->from('/grading')->post('/grading', [
            'persona_id' => 'P-001',
            'curso_id' => 'C-001',
            'valor' => 8.5,
            'observacion' => 'Excelente',
        ])->assertRedirect('/grading')->assertSessionHas('success', 'Calificación registrada correctamente.');

        $this->actingAs($user)->delete('/grading/G-001')->assertRedirect('/grading')->assertSessionHas('success', 'Calificación eliminada correctamente.');
    }

    public function test_grading_is_blocked_when_feature_gate_is_inactive(): void
    {
        Http::fake([
            'http://127.0.0.1:8001/' => Http::response([
                'product' => 'colegio-basico',
                'active_optional_features' => [],
                'academic_settings' => [],
            ], 200),
        ]);

        $user = User::create([
            'name' => 'Feature User',
            'email' => 'grading-off@example.com',
            'password' => bcrypt('secret123'),
        ]);

        $this->actingAs($user)->get('/grading')->assertNotFound();
    }

    public function test_reports_routes_render_expected_views(): void
    {
        Http::fake([
            'http://127.0.0.1:8001/' => Http::response([
                'product' => 'universidad-compleja',
                'active_optional_features' => ['reports'],
                'academic_settings' => [],
            ], 200),
            'http://127.0.0.1:8001/reports/' => Http::response(['data' => [['id' => 'R-001']]], 200),
            'http://127.0.0.1:8001/reports/consolidado/' => Http::response(['data' => [['id' => 'R-001']]], 200),
            'http://127.0.0.1:8001/reports/rendimiento/P-001' => Http::response(['reporte' => ['persona_id' => 'P-001', 'promedio' => 8.5]], 200),
        ]);

        $user = User::create([
            'name' => 'Reports User',
            'email' => 'reports@example.com',
            'password' => bcrypt('secret123'),
        ]);

        $this->actingAs($user)->get('/reports')->assertOk()->assertViewIs('reports.index');
        $this->actingAs($user)->get('/reports/consolidado')->assertOk()->assertViewIs('reports.index');
        $this->actingAs($user)->get('/reports/rendimiento/P-001')->assertOk()->assertViewIs('reports.show');
    }

    public function test_reports_are_blocked_when_feature_is_inactive(): void
    {
        Cache::flush();

        Http::fake([
            'http://127.0.0.1:8001/' => Http::response([
                'product' => 'universidad-compleja',
                'active_optional_features' => [],
                'academic_settings' => [],
            ], 200),
        ]);

        $user = User::create([
            'name' => 'Reports User',
            'email' => 'reports-inactive@example.com',
            'password' => bcrypt('secret123'),
        ]);

        $this->actingAs($user)->get('/reports')->assertNotFound();
    }
}
