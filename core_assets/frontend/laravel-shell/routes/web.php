<?php

// routes/web.php
//
// Este archivo NUNCA debe crecer con lógica de negocio. Su único
// trabajo es: 1) registrar auth genérica, 2) cargar las rutas de
// cada módulo activo. Así, agregar un módulo nuevo no obliga a tocar
// este archivo más que para un require adicional.

use App\Http\Controllers\Auth\LoginController;
use Illuminate\Support\Facades\Route;

Route::get('/login', [LoginController::class, 'showLoginForm'])->name('login');
Route::post('/login', [LoginController::class, 'login']);
Route::post('/logout', [LoginController::class, 'logout'])->name('logout');

Route::middleware('auth')->get('/dashboard', function () {
    return view('dashboard');
})->name('dashboard');

// ── Core Services (siempre activos) ────────────────────────────────────────
require base_path('app/Modules/PersonasModule/routes.php');
require base_path('app/Modules/CursosModule/routes.php');
require base_path('app/Modules/PeriodosModule/routes.php');

// ── Optional Features (las rutas están registradas, pero el controlador
//    de cada módulo aborta con 404 si la feature no está activa en el YAML.
//    Es defensa en profundidad). ─────────────────────────────────────────
require base_path('app/Modules/AttendanceModule/routes.php');
require base_path('app/Modules/GradingModule/routes.php');
require base_path('app/Modules/EnrollmentModule/routes.php');
require base_path('app/Modules/ScheduleModule/routes.php');
require base_path('app/Modules/ReportsModule/routes.php');
require base_path('app/Modules/CertificatesModule/routes.php');
