<?php

use App\Modules\ScheduleModule\Http\Controllers\ScheduleController;
use Illuminate\Support\Facades\Route;

Route::middleware(['web', 'auth'])->group(function () {
    Route::get('/schedule', [ScheduleController::class, 'index'])->name('schedule.index');
});
