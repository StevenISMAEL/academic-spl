<?php

use App\Modules\ReportsModule\Http\Controllers\ReportsController;
use Illuminate\Support\Facades\Route;

Route::middleware(['web', 'auth'])->group(function () {
    Route::get('/reports', [ReportsController::class, 'index'])->name('reports.index');
});
