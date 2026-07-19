<?php

namespace Tests\Unit\Services;

use App\Core\Services\FeatureGate;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Http;
use Tests\TestCase;

class FeatureGateTest extends TestCase
{
    protected function setUp(): void
    {
        parent::setUp();
        config(['core_engine.backend_url' => 'http://127.0.0.1:8001']);
        Cache::flush();
    }

    public function test_active_features_and_settings_are_resolved_from_backend(): void
    {
        Http::fake([
            'http://127.0.0.1:8001/' => Http::response([
                'product' => 'colegio-basico',
                'active_optional_features' => ['attendance', 'enrollment'],
                'academic_settings' => [
                    'evaluation_scale' => 'literal',
                    'passing_grade' => 7.0,
                ],
            ], 200),
        ]);

        $this->assertTrue(FeatureGate::isActive('attendance'));
        $this->assertFalse(FeatureGate::isActive('schedule'));
        $this->assertSame(['attendance', 'enrollment'], FeatureGate::activeFeatures());
        $this->assertSame('literal', FeatureGate::setting('evaluation_scale'));
        $this->assertSame(7, FeatureGate::setting('passing_grade'));
    }

    public function test_product_info_returns_fail_closed_defaults_when_backend_is_unavailable(): void
    {
        Http::fake([
            'http://127.0.0.1:8001/' => Http::response([
                'detail' => 'backend down',
            ], 500),
        ]);

        $info = FeatureGate::productInfo();

        $this->assertSame('Desconectado', $info['product']);
        $this->assertSame([], $info['active_optional_features']);
        $this->assertSame([], $info['academic_settings']);
    }
}
