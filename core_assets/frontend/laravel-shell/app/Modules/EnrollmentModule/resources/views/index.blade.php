<x-layout>
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.5rem; font-weight: 700; margin: 0; color: var(--text-dark);">
            Matrículas / Inscripciones
        </h2>
        @php $limite = \App\Core\Services\FeatureGate::setting('max_enrollments_per_period', 'N/A'); @endphp
        <p style="color: #64748b; font-size: 0.875rem; margin: 0.25rem 0 0;">
            Límite de materias por período configurado: <strong>{{ $limite }}</strong>
        </p>
    </div>

    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 2rem; align-items: start;">
        <div>
            {{-- Tabla de matrículas con acciones de cambio de estado --}}
            @if(!empty($matriculas))
                <div style="overflow-x: auto; border: 1px solid #e2e8f0; border-radius: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                    <table style="width: 100%; border-collapse: collapse; font-size: 0.875rem;">
                        <thead style="background: #f8fafc;">
                            <tr>
                                <th style="padding: 0.75rem 1rem; text-align: left; font-weight: 600; color: #374151; border-bottom: 1px solid #e5e7eb;">Persona</th>
                                <th style="padding: 0.75rem 1rem; text-align: left; font-weight: 600; color: #374151; border-bottom: 1px solid #e5e7eb;">Curso</th>
                                <th style="padding: 0.75rem 1rem; text-align: left; font-weight: 600; color: #374151; border-bottom: 1px solid #e5e7eb;">Estado</th>
                                <th style="padding: 0.75rem 1rem; text-align: center; font-weight: 600; color: #374151; border-bottom: 1px solid #e5e7eb;">Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            @foreach($matriculas as $m)
                                <tr style="border-bottom: 1px solid #f1f5f9;">
                                    <td style="padding: 0.75rem 1rem; color: #111827;">{{ $m['persona_id'] ?? '-' }}</td>
                                    <td style="padding: 0.75rem 1rem; color: #111827;">{{ $m['curso_id'] ?? '-' }}</td>
                                    <td style="padding: 0.75rem 1rem;">
                                        @php $estado = strtolower($m['estado'] ?? ''); @endphp
                                        @if($estado === 'inscrito')
                                            <span style="background:#dbeafe;color:#1e40af;font-size:0.75rem;padding:0.25rem 0.75rem;border-radius:9999px;font-weight:600;">inscrito</span>
                                        @elseif($estado === 'aprobado')
                                            <span style="background:#dcfce7;color:#166534;font-size:0.75rem;padding:0.25rem 0.75rem;border-radius:9999px;font-weight:600;">aprobado</span>
                                        @elseif($estado === 'reprobado')
                                            <span style="background:#fee2e2;color:#991b1b;font-size:0.75rem;padding:0.25rem 0.75rem;border-radius:9999px;font-weight:600;">reprobado</span>
                                        @else
                                            <span style="background:#f3f4f6;color:#374151;font-size:0.75rem;padding:0.25rem 0.75rem;border-radius:9999px;font-weight:600;">{{ $m['estado'] ?? '-' }}</span>
                                        @endif
                                    </td>
                                    <td style="padding: 0.75rem 1rem; text-align: center;">
                                        {{-- PATCH status --}}
                                        <form action="/enrollment/{{ $m['id'] }}/status" method="POST" style="display: inline-flex; gap: 0.5rem; align-items: center;">
                                            @csrf @method('PATCH')
                                            <select name="estado" aria-label="Cambiar estado" style="font-size: 0.75rem; border: 1px solid #d1d5db; border-radius: 0.25rem; padding: 0.25rem 0.5rem;">
                                                <option value="inscrito">inscrito</option>
                                                <option value="retirado">retirado</option>
                                                <option value="aprobado">aprobado</option>
                                                <option value="reprobado">reprobado</option>
                                            </select>
                                            <button type="submit" style="font-size:0.75rem;background:#0f172a;color:white;border:none;border-radius:0.25rem;padding:0.3rem 0.6rem;cursor:pointer;">
                                                Cambiar
                                            </button>
                                        </form>
                                        {{-- DELETE --}}
                                        <form action="/enrollment/{{ $m['id'] }}" method="POST" style="display: inline-block; margin-left: 0.25rem;">
                                            @csrf @method('DELETE')
                                            <button type="submit" onclick="return confirm('¿Eliminar esta matrícula?')"
                                                style="font-size:0.75rem;background:#dc2626;color:white;border:none;border-radius:0.25rem;padding:0.3rem 0.6rem;cursor:pointer;">
                                                Eliminar
                                            </button>
                                        </form>
                                    </td>
                                </tr>
                            @endforeach
                        </tbody>
                    </table>
                </div>
            @else
                <div style="text-align: center; padding: 3rem; background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 0.5rem; color: #6b7280;">
                    <p style="font-size: 2rem; margin: 0 0 0.5rem;">📋</p>
                    <p style="font-weight: 600;">No hay matrículas registradas</p>
                </div>
            @endif
        </div>

        <div>
            <h3 style="font-size: 1.125rem; font-weight: 600; margin: 0 0 1rem; color: var(--text-dark);">
                Nueva Matrícula
            </h3>
            <x-entity-form
                :fields="[
                    ['name' => 'persona_id', 'type' => 'select', 'label' => 'Estudiante', 'required' => true, 'options' => $personas],
                    ['name' => 'curso_id',   'type' => 'select', 'label' => 'Curso',      'required' => true, 'options' => $cursos]
                ]"
                action="/enrollment"
                submitLabel="Inscribir"
            />

            {{-- CA-05: error de límite de inscripciones --}}
            @if($errors->has('limite'))
                <div style="margin-top: 1rem; background: #fef3c7; border: 1px solid #fcd34d; border-radius: 0.5rem; padding: 1rem;">
                    <p style="margin: 0; color: #92400e; font-weight: 600; font-size: 0.875rem;">
                        ⚠️ Límite de inscripciones alcanzado
                    </p>
                    <p style="margin: 0.25rem 0 0; color: #78350f; font-size: 0.813rem;">
                        {{ $errors->first('limite') }}
                    </p>
                </div>
            @endif
        </div>
    </div>
</x-layout>
