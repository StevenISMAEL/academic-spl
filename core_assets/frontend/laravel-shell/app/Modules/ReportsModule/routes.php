<?php

use App\Modules\ReportsModule\Http\Controllers\ReportsController;
use Illuminate\Support\Facades\Route;

Route::middleware(['web', 'auth'])->group(function () {
    Route::get('/reports',                          [ReportsController::class, 'index'])->name('reports.index');
    Route::get('/reports/consolidado',              [ReportsController::class, 'consolidado'])->name('reports.consolidado');
    Route::get('/reports/rendimiento/{persona_id}', [ReportsController::class, 'rendimiento'])->name('reports.rendimiento');
});
