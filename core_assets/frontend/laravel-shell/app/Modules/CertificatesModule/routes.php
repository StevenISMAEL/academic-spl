<?php

use App\Modules\CertificatesModule\Http\Controllers\CertificatesController;
use Illuminate\Support\Facades\Route;

Route::middleware(['web', 'auth'])->group(function () {
    Route::get('/certificates',                          [CertificatesController::class, 'index'])->name('certificates.index');
    Route::get('/certificates/persona/{persona_id}',     [CertificatesController::class, 'byPersona'])->name('certificates.persona');
    Route::post('/certificates/{persona_id}/generate',   [CertificatesController::class, 'generate'])->name('certificates.generate');
});
