<?php

use App\Modules\EnrollmentModule\Http\Controllers\EnrollmentController;
use Illuminate\Support\Facades\Route;

Route::middleware(['web', 'auth'])->group(function () {
    Route::get('/enrollment',              [EnrollmentController::class, 'index'])->name('enrollment.index');
    Route::post('/enrollment',             [EnrollmentController::class, 'store'])->name('enrollment.store');
    Route::patch('/enrollment/{id}/status',[EnrollmentController::class, 'updateStatus'])->name('enrollment.updateStatus');
    Route::delete('/enrollment/{id}',      [EnrollmentController::class, 'destroy'])->name('enrollment.destroy');
});
