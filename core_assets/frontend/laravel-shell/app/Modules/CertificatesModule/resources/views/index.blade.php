<x-layout>
@php
    $certs    = $data['certificados'] ?? [];
    $emitidos = $data['emitidos']     ?? 0;
    $rechazados = $data['rechazados'] ?? 0;
    $requisitos = $data['requisitos'] ?? [];
    $productName = $data['product_name'] ?? '';
    $nombre  = $data['nombre'] ?? null;   // cuando se filtra por persona
@endphp

<div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.5rem;flex-wrap:wrap;">
    <h2 style="font-size:1.5rem;font-weight:700;margin:0;color:var(--text-dark);">🎓 Certificados de Aprobación</h2>
    @if($productName)
        <span style="background:#eff6ff;color:#1e40af;padding:.25rem .75rem;border-radius:9999px;font-size:.75rem;font-weight:600;">{{ $productName }}</span>
    @endif
</div>

{{-- Requisitos + Estadísticas --}}
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1rem;margin-bottom:1.5rem;">
    <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:.5rem;padding:1rem;text-align:center;">
        <div style="font-size:.7rem;font-weight:600;color:#15803d;text-transform:uppercase;">Nota Mínima</div>
        <div style="font-size:1.5rem;font-weight:700;color:#166534;">{{ $requisitos['nota_minima'] ?? '—' }}</div>
    </div>
    <div style="background:#fefce8;border:1px solid #fde68a;border-radius:.5rem;padding:1rem;text-align:center;">
        <div style="font-size:.7rem;font-weight:600;color:#a16207;text-transform:uppercase;">Asistencia Mín.</div>
        <div style="font-size:1.5rem;font-weight:700;color:#92400e;">{{ $requisitos['asistencia_minima_pct'] ?? '—' }}%</div>
    </div>
    <div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:.5rem;padding:1rem;text-align:center;">
        <div style="font-size:.7rem;font-weight:600;color:#1e40af;text-transform:uppercase;">Emitidos</div>
        <div style="font-size:1.5rem;font-weight:700;color:#1e3a8a;">{{ $emitidos }}</div>
    </div>
    <div style="background:#fef2f2;border:1px solid #fecaca;border-radius:.5rem;padding:1rem;text-align:center;">
        <div style="font-size:.7rem;font-weight:600;color:#b91c1c;text-transform:uppercase;">Rechazados</div>
        <div style="font-size:1.5rem;font-weight:700;color:#991b1b;">{{ $rechazados }}</div>
    </div>
</div>

{{-- Formulario: Generar certificado --}}
<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:.5rem;padding:1.25rem;margin-bottom:1.5rem;">
    <h3 style="font-size:1rem;font-weight:700;margin:0 0 1rem;color:var(--text-dark);">Generar Certificado</h3>
    <form method="POST" action="" id="cert-form" style="display:flex;gap:.75rem;align-items:flex-end;flex-wrap:wrap;">
        @csrf
        <div>
            <label style="display:block;font-size:.8rem;font-weight:600;color:#374151;margin-bottom:.375rem;">Estudiante</label>
            <select id="persona-select" name="persona_id"
                    style="padding:.5rem 1rem;border:1px solid #cbd5e1;border-radius:.375rem;font-size:.875rem;min-width:220px;">
                <option value="">— Seleccionar —</option>
                @foreach($personas as $p)
                    <option value="{{ $p['id'] }}">{{ $p['nombres'] ?? '' }} {{ $p['apellidos'] ?? '' }}</option>
                @endforeach
            </select>
        </div>
        <button type="button" onclick="generarCertificado()"
                style="background:#1e3a8a;color:#fff;padding:.5rem 1.25rem;border:none;border-radius:.375rem;font-size:.875rem;font-weight:600;cursor:pointer;">
            🎓 Generar
        </button>
    </form>
</div>

{{-- Tabla de certificados --}}
@if(count($certs) > 0)
    <h3 style="font-size:1rem;font-weight:700;margin:0 0 .75rem;color:var(--text-dark);">Historial de Certificados</h3>
    <table style="width:100%;border-collapse:collapse;font-size:.875rem;">
        <thead>
            <tr style="background:#f8fafc;border-bottom:2px solid #e2e8f0;">
                <th style="padding:.75rem;text-align:left;font-size:.7rem;text-transform:uppercase;color:#64748b;">Persona</th>
                <th style="padding:.75rem;text-align:center;color:#64748b;font-size:.7rem;text-transform:uppercase;">Nota Final</th>
                <th style="padding:.75rem;text-align:center;color:#64748b;font-size:.7rem;text-transform:uppercase;">Asistencia</th>
                <th style="padding:.75rem;text-align:left;color:#64748b;font-size:.7rem;text-transform:uppercase;">Estado</th>
                <th style="padding:.75rem;text-align:left;color:#64748b;font-size:.7rem;text-transform:uppercase;">Fecha</th>
                <th style="padding:.75rem;text-align:left;color:#64748b;font-size:.7rem;text-transform:uppercase;">Observación</th>
            </tr>
        </thead>
        <tbody>
            @foreach($certs as $c)
                @php
                    $esEmitido = $c['estado'] === 'emitido';
                    $color = $esEmitido ? '#15803d' : '#b91c1c';
                    $bg    = $esEmitido ? '#dcfce7'  : '#fee2e2';
                    $icon  = $esEmitido ? '✅' : '❌';
                @endphp
                <tr style="border-bottom:1px solid #f1f5f9;">
                    <td style="padding:.75rem;font-family:monospace;font-size:.8rem;">{{ $c['persona_id'] }}</td>
                    <td style="padding:.75rem;text-align:center;font-weight:600;">
                        {{ $c['nota_final'] !== null ? number_format($c['nota_final'], 2) : '—' }}
                    </td>
                    <td style="padding:.75rem;text-align:center;">
                        {{ $c['asistencia_pct'] !== null ? number_format($c['asistencia_pct'], 1).'%' : '—' }}
                    </td>
                    <td style="padding:.75rem;">
                        <span style="background:{{ $bg }};color:{{ $color }};padding:.2rem .625rem;border-radius:9999px;font-size:.75rem;font-weight:600;">
                            {{ $icon }} {{ strtoupper($c['estado']) }}
                        </span>
                    </td>
                    <td style="padding:.75rem;font-size:.8rem;color:#64748b;">{{ $c['fecha_emision'] }}</td>
                    <td style="padding:.75rem;font-size:.8rem;color:#64748b;">{{ $c['motivo_rechazo'] ?? '—' }}</td>
                </tr>
            @endforeach
        </tbody>
    </table>
@else
    <p style="color:#64748b;font-style:italic;">No hay certificados registrados aún. Usa el formulario para generar el primero.</p>
@endif

<script>
function generarCertificado() {
    const select = document.getElementById('persona-select');
    const personaId = select.value;
    if (!personaId) { alert('Selecciona un estudiante primero.'); return; }

    const form = document.getElementById('cert-form');
    form.action = '/certificates/' + personaId + '/generate';
    form.submit();
}
</script>
</x-layout>
