<?php if (isset($component)) { $__componentOriginal23a33f287873b564aaf305a1526eada4 = $component; } ?>
<?php if (isset($attributes)) { $__attributesOriginal23a33f287873b564aaf305a1526eada4 = $attributes; } ?>
<?php $component = Illuminate\View\AnonymousComponent::resolve(['view' => 'components.layout','data' => []] + (isset($attributes) && $attributes instanceof Illuminate\View\ComponentAttributeBag ? $attributes->all() : [])); ?>
<?php $component->withName('layout'); ?>
<?php if ($component->shouldRender()): ?>
<?php $__env->startComponent($component->resolveView(), $component->data()); ?>
<?php if (isset($attributes) && $attributes instanceof Illuminate\View\ComponentAttributeBag): ?>
<?php $attributes = $attributes->except(\Illuminate\View\AnonymousComponent::ignoredParameterNames()); ?>
<?php endif; ?>
<?php $component->withAttributes([]); ?>
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.5rem; font-weight: 700; margin: 0 0 0.25rem; color: var(--text-dark);">
            Calificaciones
        </h2>
        <p style="color: #64748b; font-size: 0.875rem; margin: 0;">
            Escala de evaluación: <strong><?php echo e($scale); ?></strong> &nbsp;|&nbsp;
            Nota mínima para aprobar: <strong><?php echo e($passing); ?></strong>
        </p>
    </div>

    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 2rem; align-items: start;">
        <div>
            <?php
                // Build row data from API response, adding display-friendly keys
                $tableRows = collect($notas)->map(function ($nota) {
                    return [
                        'persona_id'         => $nota['persona_id'] ?? '-',
                        'curso_id'           => $nota['curso_id'] ?? '-',
                        'valor_display'      => $nota['valor_display'] ?? $nota['valor'] ?? '-',
                        'aprueba'            => $nota['aprueba'] ?? false,
                        'estado_aprobacion'  => $nota['estado_aprobacion'] ?? '-',
                        'observacion'        => $nota['observacion'] ?? '-',
                    ];
                })->toArray();
            ?>

            <?php if (isset($component)) { $__componentOriginalc8463834ba515134d5c98b88e1a9dc03 = $component; } ?>
<?php if (isset($attributes)) { $__attributesOriginalc8463834ba515134d5c98b88e1a9dc03 = $attributes; } ?>
<?php $component = Illuminate\View\AnonymousComponent::resolve(['view' => 'components.data-table','data' => ['columns' => [
                    'persona_id'        => 'Persona',
                    'curso_id'          => 'Curso',
                    'valor_display'     => 'Nota',
                    'aprueba'           => 'Aprueba',
                    'estado_aprobacion' => 'Estado',
                    'observacion'       => 'Observación'
                ],'rows' => $tableRows,'emptyMessage' => 'No hay calificaciones registradas']] + (isset($attributes) && $attributes instanceof Illuminate\View\ComponentAttributeBag ? $attributes->all() : [])); ?>
<?php $component->withName('data-table'); ?>
<?php if ($component->shouldRender()): ?>
<?php $__env->startComponent($component->resolveView(), $component->data()); ?>
<?php if (isset($attributes) && $attributes instanceof Illuminate\View\ComponentAttributeBag): ?>
<?php $attributes = $attributes->except(\Illuminate\View\AnonymousComponent::ignoredParameterNames()); ?>
<?php endif; ?>
<?php $component->withAttributes(['columns' => \Illuminate\View\Compilers\BladeCompiler::sanitizeComponentAttribute([
                    'persona_id'        => 'Persona',
                    'curso_id'          => 'Curso',
                    'valor_display'     => 'Nota',
                    'aprueba'           => 'Aprueba',
                    'estado_aprobacion' => 'Estado',
                    'observacion'       => 'Observación'
                ]),'rows' => \Illuminate\View\Compilers\BladeCompiler::sanitizeComponentAttribute($tableRows),'emptyMessage' => 'No hay calificaciones registradas']); ?>
<?php echo $__env->renderComponent(); ?>
<?php endif; ?>
<?php if (isset($__attributesOriginalc8463834ba515134d5c98b88e1a9dc03)): ?>
<?php $attributes = $__attributesOriginalc8463834ba515134d5c98b88e1a9dc03; ?>
<?php unset($__attributesOriginalc8463834ba515134d5c98b88e1a9dc03); ?>
<?php endif; ?>
<?php if (isset($__componentOriginalc8463834ba515134d5c98b88e1a9dc03)): ?>
<?php $component = $__componentOriginalc8463834ba515134d5c98b88e1a9dc03; ?>
<?php unset($__componentOriginalc8463834ba515134d5c98b88e1a9dc03); ?>
<?php endif; ?>
        </div>

        <div>
            <h3 style="font-size: 1.125rem; font-weight: 600; margin: 0 0 1rem; color: var(--text-dark);">
                Registrar Calificación
            </h3>
            <?php if (isset($component)) { $__componentOriginalf4359a7875ba093ade2251f11a0d50c5 = $component; } ?>
<?php if (isset($attributes)) { $__attributesOriginalf4359a7875ba093ade2251f11a0d50c5 = $attributes; } ?>
<?php $component = Illuminate\View\AnonymousComponent::resolve(['view' => 'components.entity-form','data' => ['fields' => [
                    ['name' => 'persona_id', 'type' => 'select', 'label' => 'Estudiante', 'required' => true, 'options' => $personas],
                    ['name' => 'curso_id',   'type' => 'select', 'label' => 'Curso',      'required' => true, 'options' => $cursos],
                    ['name' => 'valor',      'type' => 'number', 'label' => 'Nota (0-10)', 'required' => true, 'min' => 0, 'max' => 10, 'step' => '0.1'],
                    ['name' => 'observacion','type' => 'text',   'label' => 'Observación', 'required' => false]
                ],'action' => '/grading','submitLabel' => 'Registrar Nota']] + (isset($attributes) && $attributes instanceof Illuminate\View\ComponentAttributeBag ? $attributes->all() : [])); ?>
<?php $component->withName('entity-form'); ?>
<?php if ($component->shouldRender()): ?>
<?php $__env->startComponent($component->resolveView(), $component->data()); ?>
<?php if (isset($attributes) && $attributes instanceof Illuminate\View\ComponentAttributeBag): ?>
<?php $attributes = $attributes->except(\Illuminate\View\AnonymousComponent::ignoredParameterNames()); ?>
<?php endif; ?>
<?php $component->withAttributes(['fields' => \Illuminate\View\Compilers\BladeCompiler::sanitizeComponentAttribute([
                    ['name' => 'persona_id', 'type' => 'select', 'label' => 'Estudiante', 'required' => true, 'options' => $personas],
                    ['name' => 'curso_id',   'type' => 'select', 'label' => 'Curso',      'required' => true, 'options' => $cursos],
                    ['name' => 'valor',      'type' => 'number', 'label' => 'Nota (0-10)', 'required' => true, 'min' => 0, 'max' => 10, 'step' => '0.1'],
                    ['name' => 'observacion','type' => 'text',   'label' => 'Observación', 'required' => false]
                ]),'action' => '/grading','submitLabel' => 'Registrar Nota']); ?>
<?php echo $__env->renderComponent(); ?>
<?php endif; ?>
<?php if (isset($__attributesOriginalf4359a7875ba093ade2251f11a0d50c5)): ?>
<?php $attributes = $__attributesOriginalf4359a7875ba093ade2251f11a0d50c5; ?>
<?php unset($__attributesOriginalf4359a7875ba093ade2251f11a0d50c5); ?>
<?php endif; ?>
<?php if (isset($__componentOriginalf4359a7875ba093ade2251f11a0d50c5)): ?>
<?php $component = $__componentOriginalf4359a7875ba093ade2251f11a0d50c5; ?>
<?php unset($__componentOriginalf4359a7875ba093ade2251f11a0d50c5); ?>
<?php endif; ?>
        </div>
    </div>
 <?php echo $__env->renderComponent(); ?>
<?php endif; ?>
<?php if (isset($__attributesOriginal23a33f287873b564aaf305a1526eada4)): ?>
<?php $attributes = $__attributesOriginal23a33f287873b564aaf305a1526eada4; ?>
<?php unset($__attributesOriginal23a33f287873b564aaf305a1526eada4); ?>
<?php endif; ?>
<?php if (isset($__componentOriginal23a33f287873b564aaf305a1526eada4)): ?>
<?php $component = $__componentOriginal23a33f287873b564aaf305a1526eada4; ?>
<?php unset($__componentOriginal23a33f287873b564aaf305a1526eada4); ?>
<?php endif; ?>
<?php /**PATH C:\laragon\www\academic-spl\core_assets\frontend\laravel-shell\app\Modules/GradingModule/resources/views/index.blade.php ENDPATH**/ ?>