{{-- resources/views/dashboard.blade.php --}}
{{-- Esta vista es GENÉRICA: no sabe si la está viendo un colegio o
     una universidad. Cada bloque se muestra u oculta según lo que
     responda FeatureGate, que a su vez consulta al Core Engine real. --}}

<x-layout>
    <h1>Panel — {{ \App\Core\Services\FeatureGate::productInfo()['product'] ?? 'Producto' }}</h1>

    @feature('attendance')
        <section>
            <h2>Asistencia</h2>
            <p>Aquí vive el módulo de control de asistencia.</p>
        </section>
    @endfeature

    @feature('grading')
        <section>
            <h2>Calificaciones</h2>
            <p>Escala usada: {{ \App\Core\Services\FeatureGate::setting('academic_settings.evaluation_scale', 'numeric') }}</p>
        </section>
    @endfeature

    @feature('enrollment')
        <section>
            <h2>Matrícula</h2>
            <p>Aquí vive el módulo de inscripción por créditos.</p>
        </section>
    @endfeature
</x-layout>
