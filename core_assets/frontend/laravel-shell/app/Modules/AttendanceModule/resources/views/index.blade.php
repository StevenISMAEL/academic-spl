<x-layout>
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.5rem; font-weight: 700; margin: 0; color: var(--text-dark);">
            Control de Asistencia
        </h2>
    </div>

    {{-- ── CA-03: Estadísticas globales ─────────────────────────────── --}}
    @if(!empty($estadisticas))
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 2rem;">
        {{-- Porcentaje --}}
        <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 0.75rem; padding: 1.25rem; text-align: center;">
            <p style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: #3b82f6; font-weight: 600; margin: 0 0 0.5rem;">Asistencia Global</p>
            <p style="font-size: 2rem; font-weight: 800; margin: 0; color: #1e3a8a;">{{ $estadisticas['porcentaje_asistencia'] ?? 0 }}%</p>
        </div>

        {{-- Estado general --}}
        @php
            $est = strtoupper($estadisticas['estado'] ?? '');
            $estColor = match(true) {
                str_contains($est, 'APROBADO')  => ['bg' => '#dcfce7', 'bd' => '#86efac', 'tx' => '#166534'],
                str_contains($est, 'RIESGO')    => ['bg' => '#fef3c7', 'bd' => '#fcd34d', 'tx' => '#92400e'],
                default                          => ['bg' => '#fee2e2', 'bd' => '#fca5a5', 'tx' => '#991b1b'],
            };
        @endphp
        <div style="background: {{ $estColor['bg'] }}; border: 1px solid {{ $estColor['bd'] }}; border-radius: 0.75rem; padding: 1.25rem; text-align: center;">
            <p style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: {{ $estColor['tx'] }}; font-weight: 600; margin: 0 0 0.5rem;">Estado General</p>
            <p style="font-size: 1rem; font-weight: 700; margin: 0; color: {{ $estColor['tx'] }};">{{ $estadisticas['estado'] ?? '-' }}</p>
        </div>

        {{-- Presentes / Ausentes --}}
        <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 0.75rem; padding: 1.25rem; text-align: center;">
            <p style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: #16a34a; font-weight: 600; margin: 0 0 0.5rem;">Presentes</p>
            <p style="font-size: 2rem; font-weight: 800; margin: 0; color: #15803d;">{{ $estadisticas['total_presentes'] ?? 0 }}</p>
        </div>
        <div style="background: #fff1f2; border: 1px solid #fecdd3; border-radius: 0.75rem; padding: 1.25rem; text-align: center;">
            <p style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: #e11d48; font-weight: 600; margin: 0 0 0.5rem;">Ausentes</p>
            <p style="font-size: 2rem; font-weight: 800; margin: 0; color: #be123c;">{{ $estadisticas['total_ausentes'] ?? 0 }}</p>
        </div>
    </div>

    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 0.5rem; padding: 0.75rem 1rem; margin-bottom: 2rem; font-size: 0.85rem; color: #64748b;">
        Umbral de aprobación: <strong>{{ $estadisticas['umbral_aprobado'] ?? '-' }}%</strong> &nbsp;|&nbsp;
        Umbral de riesgo: <strong>{{ $estadisticas['umbral_riesgo'] ?? '-' }}%</strong> &nbsp;|&nbsp;
        Total registros: <strong>{{ $estadisticas['total_registros'] ?? 0 }}</strong>
    </div>
    @endif

    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 2rem; align-items: start;">
        <div>
            <h3 style="font-size: 1.125rem; font-weight: 600; margin: 0 0 1rem; color: var(--text-dark);">Registros de Asistencia</h3>
            @php
                $tableRows = collect($registros)->map(fn($r) => [
                    'persona_id'   => $r['persona_id'] ?? '-',
                    'curso_id'     => $r['curso_id']   ?? '-',
                    'fecha'        => $r['fecha']       ?? '-',
                    'presente'     => $r['presente']    ?? false,
                    'justificacion'=> $r['justificacion'] ?? '-',
                ])->toArray();
            @endphp
            <x-data-table
                :columns="['persona_id' => 'Persona', 'curso_id' => 'Curso', 'fecha' => 'Fecha', 'presente' => 'Presente', 'justificacion' => 'Justificación']"
                :rows="$tableRows"
                emptyMessage="No hay registros de asistencia"
            />

            @if(!empty($resumen))
                <h3 style="font-size: 1.125rem; font-weight: 600; margin: 2rem 0 1rem; color: var(--text-dark);">Resumen por Persona</h3>
                <x-data-table
                    :columns="['persona_id' => 'Persona', 'total' => 'Total', 'presentes' => 'Presentes', 'porcentaje' => 'Asistencia %', 'estado' => 'Estado']"
                    :rows="$resumen"
                    emptyMessage="Sin resumen disponible"
                />
            @endif
        </div>

        <div>
            <h3 style="font-size: 1.125rem; font-weight: 600; margin: 0 0 1rem; color: var(--text-dark);">Registrar Asistencia</h3>
            <x-entity-form
                :fields="[
                    ['name' => 'persona_id',   'type' => 'select',   'label' => 'Estudiante',    'required' => true, 'options' => $personas],
                    ['name' => 'curso_id',     'type' => 'select',   'label' => 'Curso',          'required' => true, 'options' => $cursos],
                    ['name' => 'fecha',        'type' => 'date',     'label' => 'Fecha',          'required' => true],
                    ['name' => 'presente',     'type' => 'checkbox', 'label' => 'Presente'],
                    ['name' => 'justificacion','type' => 'text',     'label' => 'Justificación']
                ]"
                action="/attendance"
                submitLabel="Guardar Asistencia"
            />
        </div>
    </div>
</x-layout>
