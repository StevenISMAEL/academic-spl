<?php

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class AuthLoginCoverageTest extends TestCase
{
    use RefreshDatabase;

    public function test_login_form_and_successful_login_flow(): void
    {
        $user = User::create([
            'name' => 'Test User',
            'email' => 'test@example.com',
            'password' => bcrypt('secret123'),
        ]);

        $this->get('/login')->assertOk()->assertViewIs('auth.login');

        $response = $this->from('/login')->post('/login', [
            'email' => $user->email,
            'password' => 'secret123',
        ]);

        $response->assertRedirect('/dashboard');
        $this->assertAuthenticatedAs($user);

        $logout = $this->post('/logout');
        $logout->assertRedirect('/login');
        $this->assertGuest();
    }

    public function test_login_returns_validation_error_for_invalid_credentials(): void
    {
        $this->from('/login')->post('/login', [
            'email' => 'wrong@example.com',
            'password' => 'wrong-password',
        ])->assertRedirect('/login')->assertSessionHasErrors(['email']);
    }
}
