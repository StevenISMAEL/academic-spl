<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     *
     * Usa firstOrCreate para que sea idempotente: no falla si el usuario
     * ya existe (útil porque el entrypoint llama db:seed en cada arranque).
     * No usa Factory ni Faker (dependencias de --dev, no disponibles en producción).
     */
    public function run(): void
    {
        User::firstOrCreate(
            ['email' => 'admin@academic-spl.local'],
            [
                'name'               => 'Admin SPL',
                'password'           => Hash::make('admin1234'),
                'email_verified_at'  => now(),
            ]
        );
    }
}
