<x-layout>
    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 2rem; align-items: start;">
        <div>
            <h2 style="font-size: 1.5rem; font-weight: 700; margin-top: 0; margin-bottom: 1rem; color: var(--text-dark);">
                Listado de Personas
            </h2>
            <x-data-table
                :columns="['id' => 'ID', 'nombres' => 'Nombres', 'apellidos' => 'Apellidos', 'documento_identidad' => 'Cédula / Documento']"
                :rows="$personas"
                emptyMessage="No hay personas registradas en el sistema"
            />
        </div>
        <div>
            <h2 style="font-size: 1.25rem; font-weight: 700; margin-top: 0; margin-bottom: 1rem; color: var(--text-dark);">
                Nueva Persona
            </h2>
            <x-entity-form
                :fields="[
                    ['name' => 'nombres', 'type' => 'text', 'label' => 'Nombres', 'required' => true, 'placeholder' => 'Ej. Juan Carlos'],
                    ['name' => 'apellidos', 'type' => 'text', 'label' => 'Apellidos', 'required' => true, 'placeholder' => 'Ej. Pérez Gómez'],
                    ['name' => 'documento_identidad', 'type' => 'text', 'label' => 'Cédula / Identificación', 'required' => true, 'placeholder' => 'Ej. 1712345678']
                ]"
                action="/personas"
                submitLabel="Registrar Persona"
            />
        </div>
    </div>
</x-layout>
