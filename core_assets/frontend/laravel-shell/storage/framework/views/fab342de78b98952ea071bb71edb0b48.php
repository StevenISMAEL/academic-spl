<?php $attributes ??= new \Illuminate\View\ComponentAttributeBag;

$__newAttributes = [];
$__propNames = \Illuminate\View\ComponentAttributeBag::extractPropNames(([
    'fields' => [],
    'action' => '',
    'method' => 'POST',
    'submitLabel' => 'Enviar'
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
    'fields' => [],
    'action' => '',
    'method' => 'POST',
    'submitLabel' => 'Enviar'
]), 'is_string', ARRAY_FILTER_USE_KEY) as $__key => $__value) {
    $$__key = $$__key ?? $__value;
}

$__defined_vars = get_defined_vars();

foreach ($attributes->all() as $__key => $__value) {
    if (array_key_exists($__key, $__defined_vars)) unset($$__key);
}

unset($__defined_vars, $__key, $__value); ?>

<?php
    $realMethod = strtoupper($method);
    $formMethod = in_array($realMethod, ['GET', 'POST']) ? $realMethod : 'POST';
    $methodSpoof = in_array($realMethod, ['PUT', 'PATCH', 'DELETE']) ? $realMethod : null;
?>

<form action="<?php echo e($action); ?>" method="<?php echo e($formMethod); ?>" class="space-y-6 bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
    <?php echo csrf_field(); ?>
    <?php if($methodSpoof): ?>
        <?php echo method_field($methodSpoof); ?>
    <?php endif; ?>

    <div class="space-y-4">
        <?php $__currentLoopData = $fields; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $field): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
            <?php
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
            ?>

            <div class="flex flex-col">
                <label for="field-<?php echo e($name); ?>" class="text-sm font-semibold text-gray-700 mb-1">
                    <?php echo e($label); ?>

                    <?php if($required): ?>
                        <span class="text-red-500">*</span>
                    <?php endif; ?>
                </label>

                <?php if($type === 'select'): ?>
                    <select 
                        name="<?php echo e($name); ?>" 
                        id="field-<?php echo e($name); ?>"
                        <?php echo e($required ? 'required' : ''); ?>

                        class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white"
                    >
                        <option value="">Seleccione una opción...</option>
                        <?php $__currentLoopData = $options; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $key => $opt): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
                            <?php
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
                            ?>
                            <option value="<?php echo e($val); ?>" <?php echo e($value == $val ? 'selected' : ''); ?>>
                                <?php echo e($lbl); ?>

                            </option>
                        <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>
                    </select>
                <?php elseif($type === 'checkbox'): ?>
                    <div class="flex items-center">
                        <input 
                            type="checkbox" 
                            name="<?php echo e($name); ?>" 
                            id="field-<?php echo e($name); ?>"
                            value="1"
                            <?php echo e($value ? 'checked' : ''); ?>

                            class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                        >
                        <span class="ml-2 text-sm text-gray-600"><?php echo e($label); ?></span>
                    </div>
                <?php else: ?>
                    <input 
                        type="<?php echo e($type); ?>" 
                        name="<?php echo e($name); ?>" 
                        id="field-<?php echo e($name); ?>"
                        value="<?php echo e($value); ?>"
                        placeholder="<?php echo e($placeholder); ?>"
                        <?php echo e($required ? 'required' : ''); ?>

                        <?php if($min !== null): ?> min="<?php echo e($min); ?>" <?php endif; ?>
                        <?php if($max !== null): ?> max="<?php echo e($max); ?>" <?php endif; ?>
                        <?php if($step !== null): ?> step="<?php echo e($step); ?>" <?php endif; ?>
                        class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white"
                    >
                <?php endif; ?>

                <?php $__errorArgs = [$name];
$__bag = $errors->getBag($__errorArgs[1] ?? 'default');
if ($__bag->has($__errorArgs[0])) :
if (isset($message)) { $__messageOriginal = $message; }
$message = $__bag->first($__errorArgs[0]); ?>
                    <span class="text-xs text-red-600 mt-1 font-medium"><?php echo e($message); ?></span>
                <?php unset($message);
if (isset($__messageOriginal)) { $message = $__messageOriginal; }
endif;
unset($__errorArgs, $__bag); ?>
            </div>
        <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>
    </div>

    <div class="pt-4 border-t border-gray-100 flex justify-end">
        <button 
            type="submit" 
            class="px-6 py-2.5 bg-blue-600 text-white font-medium text-sm leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
        >
            <?php echo e($submitLabel); ?>

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
<?php /**PATH C:\laragon\www\academic-spl\core_assets\frontend\laravel-shell\resources\views/components/entity-form.blade.php ENDPATH**/ ?>