<?php

use App\Modules\CertificatesModule\Http\Controllers\CertificatesController;
use Illuminate\Support\Facades\Route;

Route::middleware(['web', 'auth'])->group(function () {
    Route::get('/certificates', [CertificatesController::class, 'index'])->name('certificates.index');
});
