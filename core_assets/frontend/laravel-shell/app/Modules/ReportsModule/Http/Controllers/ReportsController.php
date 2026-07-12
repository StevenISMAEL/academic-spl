<?php

namespace App\Modules\ReportsModule\Http\Controllers;

use App\Core\Services\CoreEngineClient;
use App\Core\Services\FeatureGate;
use App\Http\Controllers\Controller;

class ReportsController extends Controller
{
    public function index()
    {
        abort_unless(FeatureGate::isActive('reports'), 404);

        $client = new CoreEngineClient();
        $reportes = $client->get('/reports/');

        return view('reports.index', compact('reportes'));
    }
}
