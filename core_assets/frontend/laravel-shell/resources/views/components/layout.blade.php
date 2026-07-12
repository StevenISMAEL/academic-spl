<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Academic SPL — Core Shell</title>
    <style>
        :root {
            --primary: #1e3a8a;
            --primary-hover: #1e40af;
            --secondary: #0f172a;
            --background: #f8fafc;
            --text-main: #334155;
            --text-dark: #0f172a;
            --white: #ffffff;
            --success: #15803d;
            --error: #b91c1c;
            --warning: #b45309;
        }

        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: var(--background);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        header {
            background-color: var(--secondary);
            color: var(--white);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        .header-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }

        .logo-section {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .logo-section h1 {
            font-size: 1.25rem;
            font-weight: 700;
            margin: 0;
            letter-spacing: -0.025em;
        }

        .product-badge {
            background-color: #3b82f6;
            color: var(--white);
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        nav {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            flex-wrap: wrap;
        }

        nav a {
            color: #94a3b8;
            text-decoration: none;
            font-size: 0.875rem;
            font-weight: 500;
            padding: 0.5rem 0.75rem;
            border-radius: 0.375rem;
            transition: all 0.2s ease;
        }

        nav a:hover {
            color: var(--white);
            background-color: rgba(255, 255, 255, 0.05);
        }

        nav a.active {
            color: var(--white);
            background-color: rgba(255, 255, 255, 0.1);
        }

        .logout-btn {
            background: none;
            border: 1px solid #475569;
            color: #94a3b8;
            padding: 0.4rem 0.75rem;
            font-size: 0.825rem;
            font-weight: 500;
            border-radius: 0.375rem;
            cursor: pointer;
            transition: all 0.2s;
        }

        .logout-btn:hover {
            color: var(--white);
            border-color: var(--white);
            background-color: rgba(255, 255, 255, 0.05);
        }

        main {
            flex: 1;
            max-width: 1200px;
            width: 100%;
            margin: 0 auto;
            padding: 2rem;
            box-sizing: border-box;
        }

        .card {
            background: var(--white);
            border-radius: 0.75rem;
            border: 1px solid #e2e8f0;
            padding: 2rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px -1px rgba(0, 0, 0, 0.05);
        }

        /* Alert notifications styling */
        .alert {
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1.5rem;
            font-size: 0.875rem;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .alert-success {
            background-color: #dcfce7;
            color: var(--success);
            border: 1px solid #bbf7d0;
        }

        .alert-danger {
            background-color: #fee2e2;
            color: var(--error);
            border: 1px solid #fecaca;
        }

        .alert-warning {
            background-color: #fef3c7;
            color: var(--warning);
            border: 1px solid #fde68a;
        }

        footer {
            background-color: #0f172a;
            color: #64748b;
            text-align: center;
            padding: 1rem;
            font-size: 0.75rem;
            border-top: 1px solid #1e293b;
        }
    </style>
</head>
<body>
    <header>
        <div class="header-container">
            <div class="logo-section">
                <h1>Academic SPL</h1>
                <span class="product-badge">
                    {{ \App\Core\Services\FeatureGate::productInfo()['product'] ?? 'Producto' }}
                </span>
            </div>
            
            <nav>
                {{-- Core Services: Siempre visibles --}}
                <a href="/personas" class="{{ request()->is('personas*') ? 'active' : '' }}">Personas</a>
                <a href="/cursos" class="{{ request()->is('cursos*') ? 'active' : '' }}">Cursos</a>
                <a href="/periodos" class="{{ request()->is('periodos*') ? 'active' : '' }}">Períodos</a>

                {{-- Optional Features: Condicionales a la configuración del producto activo --}}
                @feature('grading')
                    <a href="/grading" class="{{ request()->is('grading*') ? 'active' : '' }}">Calificaciones</a>
                @endfeature

                @feature('attendance')
                    <a href="/attendance" class="{{ request()->is('attendance*') ? 'active' : '' }}">Asistencia</a>
                @endfeature

                @feature('enrollment')
                    <a href="/enrollment" class="{{ request()->is('enrollment*') ? 'active' : '' }}">Matrículas</a>
                @endfeature

                @feature('schedule')
                    <a href="/schedule" class="{{ request()->is('schedule*') ? 'active' : '' }}">Horarios</a>
                @endfeature

                @feature('reports')
                    <a href="/reports" class="{{ request()->is('reports*') ? 'active' : '' }}">Reportes</a>
                @endfeature

                @feature('certificates')
                    <a href="/certificates" class="{{ request()->is('certificates*') ? 'active' : '' }}">Certificados</a>
                @endfeature

                @auth
                    <form action="{{ route('logout') }}" method="POST" style="display: inline; margin-left: 1rem;">
                        @csrf
                        <button type="submit" class="logout-btn">Salir</button>
                    </form>
                @endauth
            </nav>
        </div>
    </header>

    <main>
        {{-- Flash Messages --}}
        @if(session('success'))
            <div class="alert alert-success">
                <span>✅</span> {{ session('success') }}
            </div>
        @endif

        @if($errors->any())
            <div class="alert alert-danger">
                <span>⚠️</span>
                <ul style="margin: 0; padding-left: 1.25rem;">
                    @foreach($errors->all() as $error)
                        <li>{{ $error }}</li>
                    @endforeach
                </ul>
            </div>
        @endif

        <div class="card">
            {{ $slot }}
        </div>
    </main>

    <footer>
        &copy; {{ date('Y') }} Academic SPL Core Assets. Todos los derechos reservados.
    </footer>
</body>
</html>
