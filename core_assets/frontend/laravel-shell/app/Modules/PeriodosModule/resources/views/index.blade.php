<x-layout>
    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 2rem; align-items: start;">
        <div>
            <h2 style="font-size: 1.5rem; font-weight: 700; margin-top: 0; margin-bottom: 1rem; color: var(--text-dark);">
                Listado de Períodos Académicos
            </h2>
            <x-data-table
                :columns="['id' => 'ID Período', 'nombre' => 'Nombre Período', 'fecha_inicio' => 'Fecha Inicio', 'fecha_fin' => 'Fecha Fin']"
                :rows="$periodos"
                emptyMessage="No hay períodos académicos registrados"
            />
        </div>
        <div>
            <h2 style="font-size: 1.25rem; font-weight: 700; margin-top: 0; margin-bottom: 1rem; color: var(--text-dark);">
                Nuevo Período
            </h2>
            <x-entity-form
                :fields="[
                    ['name' => 'id', 'type' => 'text', 'label' => 'ID Período (ej. PER-2024-A)', 'required' => true, 'placeholder' => 'Ej. PER-2024-A'],
                    ['name' => 'nombre', 'type' => 'text', 'label' => 'Nombre del período', 'required' => true, 'placeholder' => 'Ej. Año Escolar 2024 o Primer Semestre 2024'],
                    ['name' => 'fecha_inicio', 'type' => 'date', 'label' => 'Fecha de Inicio', 'required' => true],
                    ['name' => 'fecha_fin', 'type' => 'date', 'label' => 'Fecha de Fin', 'required' => true]
                ]"
                action="/periodos"
                submitLabel="Registrar Período"
            />
        </div>
    </div>
</x-layout>
