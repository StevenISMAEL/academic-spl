<?php

use App\Modules\ScheduleModule\Http\Controllers\ScheduleController;
use Illuminate\Support\Facades\Route;

Route::middleware(['web', 'auth'])->group(function () {
    Route::get('/schedule',                    [ScheduleController::class, 'index'])->name('schedule.index');
    Route::post('/schedule',                   [ScheduleController::class, 'store'])->name('schedule.store');
    Route::delete('/schedule/{schedule_id}',   [ScheduleController::class, 'destroy'])->name('schedule.destroy');
});
