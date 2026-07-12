<?php

use App\Modules\PersonasModule\Http\Controllers\PersonasController;
use Illuminate\Support\Facades\Route;

Route::middleware(['web', 'auth'])->group(function () {
    Route::get('/personas', [PersonasController::class, 'index'])->name('personas.index');
    Route::post('/personas', [PersonasController::class, 'store'])->name('personas.store');
});
