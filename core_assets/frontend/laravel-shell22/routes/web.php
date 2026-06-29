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

// Carga de rutas por módulo. Cuando un módulo se "apaga" en la
// configuración, sus rutas siguen registradas (Laravel no lee el
// YAML), pero el controlador del módulo aborta con 404 — ver
// AttendanceController::index(). Es defensa en profundidad.
require base_path('app/Modules/AttendanceModule/routes.php');
