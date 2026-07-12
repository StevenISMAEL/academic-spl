<?php

// app/Modules/AttendanceModule/routes.php

use App\Modules\AttendanceModule\Http\Controllers\AttendanceController;
use Illuminate\Support\Facades\Route;

Route::middleware(['web', 'auth'])->group(function () {
    Route::get('/attendance', [AttendanceController::class, 'index'])->name('attendance.index');
    Route::post('/attendance', [AttendanceController::class, 'store'])->name('attendance.store');
});

