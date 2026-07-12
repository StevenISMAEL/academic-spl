<x-layout>
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.5rem; font-weight: 700; margin: 0 0 0.25rem; color: var(--text-dark);">
            Calificaciones
        </h2>
        <p style="color: #64748b; font-size: 0.875rem; margin: 0;">
            Escala de evaluación: <strong>{{ $scale }}</strong> &nbsp;|&nbsp;
            Nota mínima para aprobar: <strong>{{ $passing }}</strong>
        </p>
    </div>

    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 2rem; align-items: start;">
        <div>
            @php
                // Build row data from API response, adding display-friendly keys
                $tableRows = collect($notas)->map(function ($nota) {
                    return [
                        'persona_id'         => $nota['persona_id'] ?? '-',
                        'curso_id'           => $nota['curso_id'] ?? '-',
                        'valor_display'      => $nota['valor_display'] ?? $nota['valor'] ?? '-',
                        'aprueba'            => $nota['aprueba'] ?? false,
                        'estado_aprobacion'  => $nota['estado_aprobacion'] ?? '-',
                        'observacion'        => $nota['observacion'] ?? '-',
                    ];
                })->toArray();
            @endphp

            <x-data-table
                :columns="[
                    'persona_id'        => 'Persona',
                    'curso_id'          => 'Curso',
                    'valor_display'     => 'Nota',
                    'aprueba'           => 'Aprueba',
                    'estado_aprobacion' => 'Estado',
                    'observacion'       => 'Observación'
                ]"
                :rows="$tableRows"
                emptyMessage="No hay calificaciones registradas"
            />
        </div>

        <div>
            <h3 style="font-size: 1.125rem; font-weight: 600; margin: 0 0 1rem; color: var(--text-dark);">
                Registrar Calificación
            </h3>
            <x-entity-form
                :fields="[
                    ['name' => 'persona_id', 'type' => 'select', 'label' => 'Estudiante', 'required' => true, 'options' => $personas],
                    ['name' => 'curso_id',   'type' => 'select', 'label' => 'Curso',      'required' => true, 'options' => $cursos],
                    ['name' => 'valor',      'type' => 'number', 'label' => 'Nota (0-10)', 'required' => true, 'min' => 0, 'max' => 10, 'step' => '0.1'],
                    ['name' => 'observacion','type' => 'text',   'label' => 'Observación', 'required' => false]
                ]"
                action="/grading"
                submitLabel="Registrar Nota"
            />
        </div>
    </div>
</x-layout>
