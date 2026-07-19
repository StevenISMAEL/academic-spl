<?php

namespace Tests\Unit\Services;

use App\Core\Services\CoreEngineClient;
use Exception;
use Illuminate\Support\Facades\Http;
use Tests\TestCase;

class CoreEngineClientTest extends TestCase
{
    protected function setUp(): void
    {
        parent::setUp();
        config(['core_engine.backend_url' => 'http://127.0.0.1:8001']);
    }

    public function test_get_sends_query_and_decodes_json_payload(): void
    {
        Http::fake([
            'http://127.0.0.1:8001/personas/?page=1' => Http::response([
                'data' => [['id' => 'P-001']],
            ], 200),
        ]);

        $client = new CoreEngineClient();
        $result = $client->get('/personas/', ['page' => 1]);

        $this->assertSame([['id' => 'P-001']], $result['data']);
    }

    public function test_post_and_patch_and_delete_use_expected_endpoints(): void
    {
        Http::fake([
            'http://127.0.0.1:8001/enrollment/' => Http::response(['ok' => true], 200),
            'http://127.0.0.1:8001/enrollment/ABC-1/status' => Http::response(['ok' => true], 200),
            'http://127.0.0.1:8001/enrollment/ABC-1' => Http::response(['ok' => true], 200),
        ]);

        $client = new CoreEngineClient();

        $this->assertSame(['ok' => true], $client->post('/enrollment/', ['persona_id' => 'P-001']));
        $this->assertSame(['ok' => true], $client->patch('/enrollment/ABC-1/status', ['estado' => 'aprobado']));
        $this->assertSame(['ok' => true], $client->delete('/enrollment/ABC-1'));
    }

    public function test_failed_http_response_throws_exception_with_backend_detail(): void
    {
        Http::fake([
            'http://127.0.0.1:8001/attendance/' => Http::response([
                'detail' => 'No autorizado',
            ], 401),
        ]);

        $client = new CoreEngineClient();

        $this->expectException(Exception::class);
        $this->expectExceptionMessage('No autorizado');

        $client->get('/attendance/');
    }
}
