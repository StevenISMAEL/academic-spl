<?php $attributes ??= new \Illuminate\View\ComponentAttributeBag;

$__newAttributes = [];
$__propNames = \Illuminate\View\ComponentAttributeBag::extractPropNames(([
    'columns' => [],
    'rows' => [],
    'emptyMessage' => 'No hay registros disponibles.'
]));

foreach ($attributes->all() as $__key => $__value) {
    if (in_array($__key, $__propNames)) {
        $$__key = $$__key ?? $__value;
    } else {
        $__newAttributes[$__key] = $__value;
    }
}

$attributes = new \Illuminate\View\ComponentAttributeBag($__newAttributes);

unset($__propNames);
unset($__newAttributes);

foreach (array_filter(([
    'columns' => [],
    'rows' => [],
    'emptyMessage' => 'No hay registros disponibles.'
]), 'is_string', ARRAY_FILTER_USE_KEY) as $__key => $__value) {
    $$__key = $$__key ?? $__value;
}

$__defined_vars = get_defined_vars();

foreach ($attributes->all() as $__key => $__value) {
    if (array_key_exists($__key, $__defined_vars)) unset($$__key);
}

unset($__defined_vars, $__key, $__value); ?>

<?php
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
?>

<div class="overflow-x-auto shadow-sm border border-gray-200 rounded-lg">
    <table class="min-w-full divide-y divide-gray-200 bg-white text-left text-sm text-gray-500">
        <thead class="bg-gray-50 text-xs font-semibold uppercase tracking-wider text-gray-700">
            <tr>
                <?php $__currentLoopData = $normalizedColumns; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $key => $label): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
                    <th scope="col" class="px-6 py-3 border-b border-gray-200"><?php echo e($label); ?></th>
                <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>
            </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
            <?php $__empty_1 = true; $__currentLoopData = $rows; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $row): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); $__empty_1 = false; ?>
                <tr class="hover:bg-gray-50 transition-colors">
                    <?php $__currentLoopData = $normalizedColumns; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $key => $label): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
                        <?php
                            $value = data_get($row, $key);
                        ?>
                        <td class="px-6 py-4 whitespace-nowrap text-gray-900 border-b border-gray-100">
                            <?php if($key === 'estado_aprobacion'): ?>
                                <?php if(strtoupper($value) === 'APROBADO'): ?>
                                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                        APROBADO
                                    </span>
                                <?php else: ?>
                                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                                        <?php echo e($value ?: 'REPROBADO'); ?>

                                    </span>
                                <?php endif; ?>
                            <?php elseif($key === 'estado' && (isset($row['porcentaje_asistencia']) || isset($row['fecha']))): ?>
                                
                                <?php if(strtoupper($value) === 'APROBADO'): ?>
                                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                        APROBADO
                                    </span>
                                <?php elseif(strtoupper($value) === 'EN_RIESGO' || strtoupper($value) === 'AMARILLO'): ?>
                                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                                        EN RIESGO
                                    </span>
                                <?php else: ?>
                                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                                        <?php echo e($value ?: 'REPROBADO'); ?>

                                    </span>
                                <?php endif; ?>
                            <?php elseif($key === 'aprueba'): ?>
                                <?php if($value === true || $value === 1 || $value === 'true'): ?>
                                    <span class="text-green-600 font-bold" title="Sí">✅</span>
                                <?php else: ?>
                                    <span class="text-red-600 font-bold" title="No">❌</span>
                                <?php endif; ?>
                            <?php elseif(is_bool($value)): ?>
                                <?php if($value): ?>
                                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">Sí</span>
                                <?php else: ?>
                                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">No</span>
                                <?php endif; ?>
                            <?php else: ?>
                                <?php echo e($value); ?>

                            <?php endif; ?>
                        </td>
                    <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>
                </tr>
            <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); if ($__empty_1): ?>
                <tr>
                    <td colspan="<?php echo e(count($normalizedColumns) ?: 1); ?>" class="px-6 py-10 text-center text-gray-500 bg-gray-50">
                        <div class="flex flex-col items-center justify-center">
                            <span class="text-3xl mb-2">📂</span>
                            <p class="font-medium text-gray-600"><?php echo e($emptyMessage); ?></p>
                        </div>
                    </td>
                </tr>
            <?php endif; ?>
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
<?php /**PATH C:\laragon\www\academic-spl\core_assets\frontend\laravel-shell\resources\views/components/data-table.blade.php ENDPATH**/ ?>