<?php

use App\Modules\GradingModule\Http\Controllers\GradingController;
use Illuminate\Support\Facades\Route;

Route::middleware(['web', 'auth'])->group(function () {
    Route::get('/grading', [GradingController::class, 'index'])->name('grading.index');
    Route::post('/grading', [GradingController::class, 'store'])->name('grading.store');
    Route::delete('/grading/{id}', [GradingController::class, 'destroy'])->name('grading.destroy');
});
