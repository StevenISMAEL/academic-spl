<x-layout>
@php
    $config = $reporte['configuracion_aplicada'] ?? [];
    $notas  = $reporte['notas'] ?? [];
    $att    = $reporte['asistencia'] ?? [];
    $resNotas = $reporte['resumen_notas'] ?? [];
    $estado = $reporte['estado_final'] ?? 'SIN_DATOS';

    $estadoColor = match($estado) {
        'APROBADO'        => '#15803d',
        'REPROBADO_NOTA'  => '#b91c1c',
        'REPROBADO_FALTA' => '#c2410c',
        'EN_RIESGO'       => '#b45309',
        default           => '#475569',
    };
    $estadoBg = match($estado) {
        'APROBADO'        => '#dcfce7',
        'REPROBADO_NOTA'  => '#fee2e2',
        'REPROBADO_FALTA' => '#ffedd5',
        'EN_RIESGO'       => '#fef3c7',
        default           => '#f1f5f9',
    };
@endphp

<div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.5rem;flex-wrap:wrap;">
    <a href="/reports" style="color:#3b82f6;font-size:.875rem;text-decoration:none;">← Volver a Reportes</a>
    <h2 style="font-size:1.25rem;font-weight:700;margin:0;color:var(--text-dark);">
        📄 Reporte de {{ $reporte['nombre_completo'] ?? $reporte['persona_id'] ?? '—' }}
    </h2>
    <span style="background:{{ $estadoBg }};color:{{ $estadoColor }};padding:.375rem 1rem;border-radius:9999px;font-size:.875rem;font-weight:700;margin-left:auto;">
        {{ $estado }}
    </span>
</div>

{{-- Cards de resumen --}}
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1rem;margin-bottom:1.5rem;">
    <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:.5rem;padding:1rem;text-align:center;">
        <div style="font-size:.7rem;font-weight:600;color:#15803d;text-transform:uppercase;">Promedio</div>
        <div style="font-size:1.5rem;font-weight:700;color:#166534;">
            {{ $resNotas['promedio'] !== null ? number_format($resNotas['promedio'], 2) : '—' }}
        </div>
        <div style="font-size:.75rem;color:#16a34a;">Nota mín: {{ $config['passing_grade'] ?? '—' }}</div>
    </div>
    <div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:.5rem;padding:1rem;text-align:center;">
        <div style="font-size:.7rem;font-weight:600;color:#1e40af;text-transform:uppercase;">Notas</div>
        <div style="font-size:1.5rem;font-weight:700;color:#1e3a8a;">{{ $resNotas['aprobadas'] ?? 0 }}/{{ $resNotas['total'] ?? 0 }}</div>
        <div style="font-size:.75rem;color:#3b82f6;">aprobadas</div>
    </div>
    <div style="background:#fefce8;border:1px solid #fde68a;border-radius:.5rem;padding:1rem;text-align:center;">
        <div style="font-size:.7rem;font-weight:600;color:#a16207;text-transform:uppercase;">Asistencia</div>
        <div style="font-size:1.5rem;font-weight:700;color:#92400e;">
            {{ $att['porcentaje_asistencia'] !== null ? number_format($att['porcentaje_asistencia'], 1).'%' : '—' }}
        </div>
        <div style="font-size:.75rem;color:#b45309;">Mín: {{ $att['umbral_aprobado'] ?? '—' }}%</div>
    </div>
    <div style="background:#f5f3ff;border:1px solid #ddd6fe;border-radius:.5rem;padding:1rem;text-align:center;">
        <div style="font-size:.7rem;font-weight:600;color:#6d28d9;text-transform:uppercase;">Estado Asistencia</div>
        <div style="font-size:.9rem;font-weight:700;color:#4c1d95;margin-top:.5rem;">{{ $att['estado'] ?? '—' }}</div>
    </div>
</div>

{{-- Tabla de notas --}}
@if(count($notas) > 0)
    <h3 style="font-size:1rem;font-weight:700;margin:0 0 .75rem;color:var(--text-dark);">Detalle de Calificaciones</h3>
    <table style="width:100%;border-collapse:collapse;font-size:.875rem;margin-bottom:1.5rem;">
        <thead>
            <tr style="background:#f8fafc;border-bottom:2px solid #e2e8f0;">
                <th style="padding:.625rem;text-align:left;font-size:.7rem;text-transform:uppercase;color:#64748b;">Curso</th>
                <th style="padding:.625rem;text-align:center;color:#64748b;font-size:.7rem;text-transform:uppercase;">Valor</th>
                <th style="padding:.625rem;text-align:center;color:#64748b;font-size:.7rem;text-transform:uppercase;">Display</th>
                <th style="padding:.625rem;text-align:center;color:#64748b;font-size:.7rem;text-transform:uppercase;">Estado</th>
            </tr>
        </thead>
        <tbody>
            @foreach($notas as $nota)
                @php
                    $aprueba = $nota['aprueba'] ?? false;
                    $nColor  = $aprueba ? '#15803d' : '#b91c1c';
                    $nBg     = $aprueba ? '#dcfce7'  : '#fee2e2';
                @endphp
                <tr style="border-bottom:1px solid #f1f5f9;">
                    <td style="padding:.625rem;">{{ $nota['curso_id'] ?? '—' }}</td>
                    <td style="padding:.625rem;text-align:center;font-weight:600;">{{ number_format($nota['valor'], 2) }}</td>
                    <td style="padding:.625rem;text-align:center;">{{ $nota['valor_display'] ?? $nota['valor'] }}</td>
                    <td style="padding:.625rem;text-align:center;">
                        <span style="background:{{ $nBg }};color:{{ $nColor }};padding:.2rem .5rem;border-radius:9999px;font-size:.75rem;font-weight:600;">
                            {{ $nota['estado_aprobacion'] ?? ($aprueba ? 'APROBADO' : 'REPROBADO') }}
                        </span>
                    </td>
                </tr>
            @endforeach
        </tbody>
    </table>
@else
    <p style="color:#64748b;font-style:italic;margin-bottom:1.5rem;">Sin calificaciones registradas.</p>
@endif
</x-layout>
