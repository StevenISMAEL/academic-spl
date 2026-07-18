@props([
    'fields' => [],
    'action' => '',
    'method' => 'POST',
    'submitLabel' => 'Enviar'
])

@php
    $realMethod = strtoupper($method);
    $formMethod = in_array($realMethod, ['GET', 'POST']) ? $realMethod : 'POST';
    $methodSpoof = in_array($realMethod, ['PUT', 'PATCH', 'DELETE']) ? $realMethod : null;
@endphp

<form action="{{ $action }}" method="{{ $formMethod }}" class="space-y-6 bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
    @csrf
    @if($methodSpoof)
        @method($methodSpoof)
    @endif

    <div class="space-y-4">
        @foreach($fields as $field)
            @php
                $name = data_get($field, 'name');
                $type = data_get($field, 'type', 'text');
                $label = data_get($field, 'label', ucfirst($name));
                $required = data_get($field, 'required', false);
                $value = data_get($field, 'value', old($name));
                $min = data_get($field, 'min');
                $max = data_get($field, 'max');
                $step = data_get($field, 'step');
                $placeholder = data_get($field, 'placeholder', '');
                $options = data_get($field, 'options', []);
                // Generate a unique ID to prevent WCAG duplicate ID violations
                $uniqueId = 'field-' . $name . '-' . uniqid();
            @endphp

            <div class="flex flex-col">
                <label for="{{ $uniqueId }}" class="text-sm font-semibold text-gray-700 mb-1">
                    {{ $label }}
                    @if($required)
                        <span class="text-red-500">*</span>
                    @endif
                </label>

                @if($type === 'select')
                    <select 
                        name="{{ $name }}" 
                        id="{{ $uniqueId }}"
                        {{ $required ? 'required' : '' }}
                        class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white"
                    >
                        <option value="">Seleccione una opción...</option>
                        @foreach($options as $key => $opt)
                            @php
                                $val = (is_array($opt) || is_object($opt)) ? (data_get($opt, 'id') ?? data_get($opt, 'value')) : $key;
                                
                                // Resolve label
                                $lbl = '';
                                if (is_array($opt) || is_object($opt)) {
                                    $nombres = data_get($opt, 'nombres');
                                    $apellidos = data_get($opt, 'apellidos');
                                    if ($nombres && $apellidos) {
                                        $lbl = $nombres . ' ' . $apellidos;
                                    } else {
                                        $lbl = data_get($opt, 'nombre') ?? data_get($opt, 'nombres') ?? data_get($opt, 'label') ?? data_get($opt, 'name') ?? $val;
                                    }
                                } else {
                                    $lbl = $opt;
                                }

                                if (is_numeric($key) && !(is_array($opt) || is_object($opt))) {
                                    $val = $opt;
                                }
                            @endphp
                            <option value="{{ $val }}" {{ $value == $val ? 'selected' : '' }}>
                                {{ $lbl }}
                            </option>
                        @endforeach
                    </select>
                @elseif($type === 'checkbox')
                    <div class="flex items-center">
                        <input 
                            type="checkbox" 
                            name="{{ $name }}" 
                            id="{{ $uniqueId }}"
                            value="1"
                            {{ $value ? 'checked' : '' }}
                            class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                        >
                        {{-- WCAG2-A: usar <label for="..."> en lugar de <span> para asociar
                             el texto al input y que los lectores de pantalla lo anuncien. --}}
                        <label for="{{ $uniqueId }}" class="ml-2 text-sm text-gray-600 cursor-pointer">
                            {{ $label }}
                        </label>
                    </div>
                @else
                    <input 
                        type="{{ $type }}" 
                        name="{{ $name }}" 
                        id="{{ $uniqueId }}"
                        value="{{ $value }}"
                        placeholder="{{ $placeholder }}"
                        {{ $required ? 'required' : '' }}
                        @if($min !== null) min="{{ $min }}" @endif
                        @if($max !== null) max="{{ $max }}" @endif
                        @if($step !== null) step="{{ $step }}" @endif
                        class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white"
                    >
                @endif

                @error($name)
                    <span class="text-xs text-red-600 mt-1 font-medium">{{ $message }}</span>
                @enderror
            </div>
        @endforeach
    </div>

    <div class="pt-4 border-t border-gray-100 flex justify-end">
        <button 
            type="submit" 
            class="px-6 py-2.5 bg-blue-600 text-white font-medium text-sm leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
        >
            {{ $submitLabel }}
        </button>
    </div>
</form>

<style>
    /* Styling elements for modern layout */
    .space-y-6 > :not([hidden]) ~ :not([hidden]) { margin-top: 1.5rem; }
    .space-y-4 > :not([hidden]) ~ :not([hidden]) { margin-top: 1rem; }
    .flex-col { display: flex; flex-direction: column; }
    .mb-1 { margin-bottom: 0.25rem; }
    .ml-2 { margin-left: 0.5rem; }
    .pt-4 { padding-top: 1rem; }
    .flex { display: flex; }
    .justify-end { justify-content: flex-end; }
    .w-full { width: 100%; }
    .px-4 { padding-left: 1rem; padding-right: 1rem; }
    .py-2 { padding-top: 0.5rem; padding-bottom: 0.5rem; }
    .px-6 { padding-left: 1.5rem; padding-right: 1.5rem; }
    .py-2\.5 { padding-top: 0.625rem; padding-bottom: 0.625rem; }
    .border { border-style: solid; border-width: 1px; }
    .border-gray-300 { border-color: #d1d5db; }
    .rounded-md { border-radius: 0.375rem; }
    .rounded { border-radius: 0.25rem; }
    .h-4 { height: 1rem; }
    .w-4 { width: 1rem; }
    .text-blue-600 { color: #2563eb; }
    .bg-blue-600 { background-color: #2563eb; }
    .bg-blue-600:hover { background-color: #1d4ed8; }
</style>
