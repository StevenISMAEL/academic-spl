<?php

// app/Modules/AuditingModule/routes.php

use App\Modules\AuditingModule\Http\Controllers\AuditingController;
use Illuminate\Support\Facades\Route;

Route::middleware(['web', 'auth'])->group(function () {
    Route::get('/auditing', [AuditingController::class, 'index'])->name('auditing.index');
});
