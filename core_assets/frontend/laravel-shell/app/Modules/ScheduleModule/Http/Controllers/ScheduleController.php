<?php

namespace App\Modules\ScheduleModule\Http\Controllers;

use App\Core\Services\CoreEngineClient;
use App\Core\Services\FeatureGate;
use App\Http\Controllers\Controller;

class ScheduleController extends Controller
{
    public function index()
    {
        abort_unless(FeatureGate::isActive('schedule'), 404);

        $client = new CoreEngineClient();
        $horarios = $client->get('/schedule/');

        return view('schedule.index', compact('horarios'));
    }
}
