<?php

// app/Modules/AttendanceModule/routes.php
//
// Cada módulo define sus propias rutas en su propia carpeta. El
// archivo routes/web.php principal solo necesita un require de los
// módulos que existan — nunca define rutas de negocio directamente.

use App\Modules\AttendanceModule\Http\Controllers\AttendanceController;
use Illuminate\Support\Facades\Route;

Route::middleware(['web', 'auth'])->group(function () {
    Route::get('/attendance', [AttendanceController::class, 'index'])->name('attendance.index');
});
