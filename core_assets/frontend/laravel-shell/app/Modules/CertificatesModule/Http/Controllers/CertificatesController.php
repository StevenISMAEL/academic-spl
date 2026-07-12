<?php

namespace App\Modules\CertificatesModule\Http\Controllers;

use App\Core\Services\CoreEngineClient;
use App\Core\Services\FeatureGate;
use App\Http\Controllers\Controller;

class CertificatesController extends Controller
{
    public function index()
    {
        abort_unless(FeatureGate::isActive('certificates'), 404);

        $client = new CoreEngineClient();
        $certificados = $client->get('/certificates/');

        return view('certificates.index', compact('certificados'));
    }
}
