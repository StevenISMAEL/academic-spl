@props([
    'columns' => [],
    'rows' => [],
    'emptyMessage' => 'No hay registros disponibles.'
])

@php
    // Detect if columns are sequential or associative
    $isAssociative = !empty($columns) && array_keys($columns) !== range(0, count($columns) - 1);
    
    // Normalise columns to associative key => label
    $normalizedColumns = [];
    if ($isAssociative) {
        $normalizedColumns = $columns;
    } else {
        // If sequential, map them to keys of the first row if available, otherwise just use indexes
        $firstRow = reset($rows);
        $rowKeys = $firstRow ? array_keys((array) $firstRow) : [];
        
        foreach ($columns as $index => $label) {
            $key = $rowKeys[$index] ?? $index;
            $normalizedColumns[$key] = $label;
        }
    }
@endphp

<div class="overflow-x-auto shadow-sm border border-gray-200 rounded-lg">
    <table class="min-w-full divide-y divide-gray-200 bg-white text-left text-sm text-gray-500">
        <thead class="bg-gray-50 text-xs font-semibold uppercase tracking-wider text-gray-700">
            <tr>
                @foreach($normalizedColumns as $key => $label)
                    <th scope="col" class="px-6 py-3 border-b border-gray-200">{{ $label }}</th>
                @endforeach
            </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
            @forelse($rows as $row)
                <tr class="hover:bg-gray-50 transition-colors">
                    @foreach($normalizedColumns as $key => $label)
                        @php
                            $value = data_get($row, $key);
                        @endphp
                        <td class="px-6 py-4 whitespace-nowrap text-gray-900 border-b border-gray-100">
                            @if($key === 'estado_aprobacion')
                                @if(strtoupper($value) === 'APROBADO')
                                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                        APROBADO
                                    </span>
                                @else
                                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                                        {{ $value ?: 'REPROBADO' }}
                                    </span>
                                @endif
                            @elseif($key === 'estado' && (isset($row['porcentaje_asistencia']) || isset($row['fecha'])))
                                {{-- Checks if it's the attendance status --}}
                                @if(strtoupper($value) === 'APROBADO')
                                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                        APROBADO
                                    </span>
                                @elseif(strtoupper($value) === 'EN_RIESGO' || strtoupper($value) === 'AMARILLO')
                                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                                        EN RIESGO
                                    </span>
                                @else
                                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                                        {{ $value ?: 'REPROBADO' }}
                                    </span>
                                @endif
                            @elseif($key === 'aprueba')
                                @if($value === true || $value === 1 || $value === 'true')
                                    <span class="text-green-600 font-bold" title="Sí">✅</span>
                                @else
                                    <span class="text-red-600 font-bold" title="No">❌</span>
                                @endif
                            @elseif(is_bool($value))
                                @if($value)
                                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">Sí</span>
                                @else
                                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">No</span>
                                @endif
                            @else
                                {{ $value }}
                            @endif
                        </td>
                    @endforeach
                </tr>
            @empty
                <tr>
                    <td colspan="{{ count($normalizedColumns) ?: 1 }}" class="px-6 py-10 text-center text-gray-500 bg-gray-50">
                        <div class="flex flex-col items-center justify-center">
                            <span class="text-3xl mb-2">📂</span>
                            <p class="font-medium text-gray-600">{{ $emptyMessage }}</p>
                        </div>
                    </td>
                </tr>
            @endforelse
        </tbody>
    </table>
</div>

<style>
    /* Styling elements for a premium presentation */
    .bg-green-100 { background-color: #d1fae5; }
    .text-green-800 { color: #065f46; }
    .bg-red-100 { background-color: #fee2e2; }
    .text-red-800 { color: #991b1b; }
    .bg-yellow-100 { background-color: #fef3c7; }
    .text-yellow-800 { color: #92400e; }
    .bg-gray-100 { background-color: #f3f4f6; }
    .text-gray-800 { color: #374151; }
    .inline-flex { display: inline-flex; }
    .items-center { align-items: center; }
    .px-2\.5 { padding-left: 0.625rem; padding-right: 0.625rem; }
    .py-0\.5 { padding-top: 0.125rem; padding-bottom: 0.125rem; }
    .rounded-full { border-radius: 9999px; }
    .text-xs { font-size: 0.75rem; }
    .font-medium { font-weight: 500; }
    .shadow-sm { box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); }
    .border-gray-200 { border-color: #e5e7eb; }
    .divide-gray-200 > :not([hidden]) ~ :not([hidden]) { border-color: #e5e7eb; }
    .bg-gray-50 { background-color: #f9fafb; }
    .hover\:bg-gray-50:hover { background-color: #f9fafb; }
    .transition-colors { transition-property: background-color, border-color, color, fill, stroke; transition-duration: 150ms; }
    .text-gray-900 { color: #111827; }
    .border-b { border-bottom-width: 1px; }
    .border-gray-100 { border-color: #f3f4f6; }
    .font-semibold { font-weight: 600; }
    .uppercase { text-transform: uppercase; }
    .tracking-wider { letter-spacing: 0.05em; }
    .text-gray-700 { color: #374151; }
</style>
