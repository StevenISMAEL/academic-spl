<?php

use App\Modules\PeriodosModule\Http\Controllers\PeriodosController;
use Illuminate\Support\Facades\Route;

Route::middleware(['web', 'auth'])->group(function () {
    Route::get('/periodos', [PeriodosController::class, 'index'])->name('periodos.index');
    Route::post('/periodos', [PeriodosController::class, 'store'])->name('periodos.store');
});
