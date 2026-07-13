<x-layout>
@php
    $horarios      = $data['horarios']          ?? [];
    $horariosPorDia = $data['horarios_por_dia'] ?? [];
    $periodsPerYear = $data['periods_per_year'] ?? 2;
    $productName    = $data['product_name']     ?? '';
    $diasValidos    = $data['dias_validos']      ?? ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado'];
@endphp

<div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.5rem;flex-wrap:wrap;">
    <h2 style="font-size:1.5rem;font-weight:700;margin:0;color:var(--text-dark);">🗓 Horarios de Clases</h2>
    <span style="background:#eff6ff;color:#1e40af;padding:.25rem .75rem;border-radius:9999px;font-size:.75rem;font-weight:600;">
        {{ $productName }} · {{ $periodsPerYear }} período(s)/año
    </span>
    <span style="margin-left:auto;background:#f0fdf4;color:#15803d;padding:.25rem .75rem;border-radius:9999px;font-size:.75rem;font-weight:600;">
        {{ count($horarios) }} horarios registrados
    </span>
</div>

{{-- Formulario de creación --}}
<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:.5rem;padding:1.25rem;margin-bottom:1.5rem;">
    <h3 style="font-size:1rem;font-weight:700;margin:0 0 1rem;color:var(--text-dark);">Agregar Bloque de Horario</h3>
    <form method="POST" action="{{ route('schedule.store') }}" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:.75rem;align-items:end;">
        @csrf
        <div>
            <label style="display:block;font-size:.8rem;font-weight:600;color:#374151;margin-bottom:.375rem;">Curso *</label>
            <select name="curso_id" required style="width:100%;padding:.5rem;border:1px solid #cbd5e1;border-radius:.375rem;font-size:.875rem;box-sizing:border-box;">
                <option value="">— Seleccionar —</option>
                @foreach($cursos as $c)
                    <option value="{{ $c['id'] }}">{{ $c['nombre'] }}</option>
                @endforeach
            </select>
        </div>
        <div>
            <label style="display:block;font-size:.8rem;font-weight:600;color:#374151;margin-bottom:.375rem;">Día *</label>
            <select name="dia_semana" required style="width:100%;padding:.5rem;border:1px solid #cbd5e1;border-radius:.375rem;font-size:.875rem;box-sizing:border-box;">
                <option value="">— Seleccionar —</option>
                @foreach($diasValidos as $dia)
                    <option value="{{ $dia }}">{{ $dia }}</option>
                @endforeach
            </select>
        </div>
        <div>
            <label style="display:block;font-size:.8rem;font-weight:600;color:#374151;margin-bottom:.375rem;">Hora Inicio *</label>
            <input type="time" name="hora_inicio" required
                   style="width:100%;padding:.5rem;border:1px solid #cbd5e1;border-radius:.375rem;font-size:.875rem;box-sizing:border-box;">
        </div>
        <div>
            <label style="display:block;font-size:.8rem;font-weight:600;color:#374151;margin-bottom:.375rem;">Hora Fin *</label>
            <input type="time" name="hora_fin" required
                   style="width:100%;padding:.5rem;border:1px solid #cbd5e1;border-radius:.375rem;font-size:.875rem;box-sizing:border-box;">
        </div>
        <div>
            <label style="display:block;font-size:.8rem;font-weight:600;color:#374151;margin-bottom:.375rem;">Aula</label>
            <input type="text" name="aula" placeholder="Ej: A-101"
                   style="width:100%;padding:.5rem;border:1px solid #cbd5e1;border-radius:.375rem;font-size:.875rem;box-sizing:border-box;">
        </div>
        <div style="display:flex;align-items:flex-end;">
            <button type="submit"
                    style="width:100%;background:#1e3a8a;color:#fff;padding:.55rem 1rem;border:none;border-radius:.375rem;font-size:.875rem;font-weight:600;cursor:pointer;">
                ➕ Agregar
            </button>
        </div>
    </form>
</div>

{{-- Vista por día --}}
@if(count($horariosPorDia) > 0)
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:1rem;margin-bottom:1.5rem;">
        @foreach($horariosPorDia as $dia => $bloques)
            <div style="background:#fff;border:1px solid #e2e8f0;border-radius:.5rem;overflow:hidden;">
                <div style="background:#1e3a8a;color:#fff;padding:.625rem 1rem;font-weight:700;font-size:.875rem;">
                    📅 {{ $dia }}
                    <span style="float:right;background:rgba(255,255,255,.2);padding:.1rem .5rem;border-radius:9999px;font-size:.75rem;">{{ count($bloques) }}</span>
                </div>
                @foreach($bloques as $b)
                    <div style="padding:.75rem 1rem;border-bottom:1px solid #f1f5f9;display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <div style="font-weight:600;font-size:.875rem;">{{ $b['hora_inicio'] }} – {{ $b['hora_fin'] }}</div>
                            <div style="font-size:.8rem;color:#64748b;">{{ $b['nombre_curso'] ?? $b['curso_id'] }}</div>
                            @if($b['aula'])
                                <div style="font-size:.75rem;color:#94a3b8;">Aula: {{ $b['aula'] }}</div>
                            @endif
                        </div>
                        <form method="POST" action="{{ route('schedule.destroy', $b['id']) }}" onsubmit="return confirm('¿Eliminar este horario?')">
                            @csrf
                            @method('DELETE')
                            <button type="submit"
                                    style="background:#fee2e2;color:#b91c1c;border:none;padding:.3rem .6rem;border-radius:.375rem;font-size:.75rem;cursor:pointer;">
                                🗑
                            </button>
                        </form>
                    </div>
                @endforeach
            </div>
        @endforeach
    </div>
@endif

{{-- Tabla completa --}}
@if(count($horarios) > 0)
    <h3 style="font-size:1rem;font-weight:700;margin:0 0 .75rem;color:var(--text-dark);">Lista Completa</h3>
    <table style="width:100%;border-collapse:collapse;font-size:.875rem;">
        <thead>
            <tr style="background:#f8fafc;border-bottom:2px solid #e2e8f0;">
                <th style="padding:.75rem;text-align:left;font-size:.7rem;text-transform:uppercase;color:#64748b;">Curso</th>
                <th style="padding:.75rem;text-align:center;color:#64748b;font-size:.7rem;text-transform:uppercase;">Día</th>
                <th style="padding:.75rem;text-align:center;color:#64748b;font-size:.7rem;text-transform:uppercase;">Inicio</th>
                <th style="padding:.75rem;text-align:center;color:#64748b;font-size:.7rem;text-transform:uppercase;">Fin</th>
                <th style="padding:.75rem;text-align:center;color:#64748b;font-size:.7rem;text-transform:uppercase;">Aula</th>
                <th style="padding:.75rem;text-align:center;color:#64748b;font-size:.7rem;text-transform:uppercase;">Acción</th>
            </tr>
        </thead>
        <tbody>
            @foreach($horarios as $h)
                <tr style="border-bottom:1px solid #f1f5f9;">
                    <td style="padding:.75rem;font-weight:500;">{{ $h['nombre_curso'] ?? $h['curso_id'] }}</td>
                    <td style="padding:.75rem;text-align:center;">
                        <span style="background:#eff6ff;color:#1e40af;padding:.2rem .5rem;border-radius:9999px;font-size:.75rem;font-weight:600;">{{ $h['dia_semana'] }}</span>
                    </td>
                    <td style="padding:.75rem;text-align:center;">{{ $h['hora_inicio'] }}</td>
                    <td style="padding:.75rem;text-align:center;">{{ $h['hora_fin'] }}</td>
                    <td style="padding:.75rem;text-align:center;color:#64748b;">{{ $h['aula'] ?? '—' }}</td>
                    <td style="padding:.75rem;text-align:center;">
                        <form method="POST" action="{{ route('schedule.destroy', $h['id']) }}" onsubmit="return confirm('¿Eliminar?')" style="display:inline;">
                            @csrf
                            @method('DELETE')
                            <button type="submit" style="background:#fee2e2;color:#b91c1c;border:none;padding:.3rem .75rem;border-radius:.375rem;font-size:.8rem;cursor:pointer;">
                                Eliminar
                            </button>
                        </form>
                    </td>
                </tr>
            @endforeach
        </tbody>
    </table>
@else
    <p style="color:#64748b;font-style:italic;">No hay horarios registrados aún. Agrega el primer bloque usando el formulario.</p>
@endif
</x-layout>
