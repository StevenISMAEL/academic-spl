<x-layout>
    <h1>Auditoría del Sistema</h1>
    <p>Historial de acciones registradas.</p>

    <div class="mt-4">
        <h3>Registros Recientes</h3>
        @if(empty($registros))
            <p>No hay registros de auditoría.</p>
        @else
            <table class="table-auto w-full mt-4 border-collapse border border-gray-200">
                <thead>
                    <tr class="bg-gray-100">
                        <th class="border px-4 py-2">ID</th>
                        <th class="border px-4 py-2">Usuario ID</th>
                        <th class="border px-4 py-2">Acción</th>
                        <th class="border px-4 py-2">Entidad</th>
                        <th class="border px-4 py-2">Entidad ID</th>
                        <th class="border px-4 py-2">Fecha/Hora</th>
                    </tr>
                </thead>
                <tbody>
                    @foreach($registros as $log)
                        <tr>
                            <td class="border px-4 py-2">{{ $log['id'] ?? '' }}</td>
                            <td class="border px-4 py-2">{{ $log['usuario_id'] ?? '' }}</td>
                            <td class="border px-4 py-2">{{ $log['accion'] ?? '' }}</td>
                            <td class="border px-4 py-2">{{ $log['entidad'] ?? '' }}</td>
                            <td class="border px-4 py-2">{{ $log['entidad_id'] ?? '' }}</td>
                            <td class="border px-4 py-2">{{ $log['fecha_hora'] ?? '' }}</td>
                        </tr>
                    @endforeach
                </tbody>
            </table>
        @endif
    </div>
</x-layout>
