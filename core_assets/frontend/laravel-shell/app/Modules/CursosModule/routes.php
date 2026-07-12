<?php

use App\Modules\CursosModule\Http\Controllers\CursosController;
use Illuminate\Support\Facades\Route;

Route::middleware(['web', 'auth'])->group(function () {
    Route::get('/cursos', [CursosController::class, 'index'])->name('cursos.index');
    Route::post('/cursos', [CursosController::class, 'store'])->name('cursos.store');
});
