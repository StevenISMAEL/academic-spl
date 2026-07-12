<x-layout>
    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 2rem; align-items: start;">
        <div>
            <h2 style="font-size: 1.5rem; font-weight: 700; margin-top: 0; margin-bottom: 1rem; color: var(--text-dark);">
                Listado de Cursos
            </h2>
            <x-data-table
                :columns="['id' => 'ID del Curso', 'nombre' => 'Nombre del Curso', 'periodo_id' => 'ID Período']"
                :rows="$cursos"
                emptyMessage="No hay cursos registrados en el sistema"
            />
        </div>
        <div>
            <h2 style="font-size: 1.25rem; font-weight: 700; margin-top: 0; margin-bottom: 1rem; color: var(--text-dark);">
                Nuevo Curso
            </h2>
            <x-entity-form
                :fields="[
                    ['name' => 'id', 'type' => 'text', 'label' => 'ID único (ej. C-MAT)', 'required' => true, 'placeholder' => 'Ej. C-MAT'],
                    ['name' => 'nombre', 'type' => 'text', 'label' => 'Nombre del curso', 'required' => true, 'placeholder' => 'Ej. Matemáticas'],
                    ['name' => 'periodo_id', 'type' => 'select', 'label' => 'Período Académico', 'required' => true, 'options' => $periodos]
                ]"
                action="/cursos"
                submitLabel="Registrar Curso"
            />
        </div>
    </div>
</x-layout>
