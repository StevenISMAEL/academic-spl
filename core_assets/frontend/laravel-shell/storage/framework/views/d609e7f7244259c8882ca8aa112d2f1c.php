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
        <h2 style="font-size: 1.5rem; font-weight: 700; margin: 0; color: var(--text-dark);">
            Control de Asistencia
        </h2>
    </div>

    
    <?php if(!empty($estadisticas)): ?>
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 2rem;">
        
        <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 0.75rem; padding: 1.25rem; text-align: center;">
            <p style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: #3b82f6; font-weight: 600; margin: 0 0 0.5rem;">Asistencia Global</p>
            <p style="font-size: 2rem; font-weight: 800; margin: 0; color: #1e3a8a;"><?php echo e($estadisticas['porcentaje_asistencia'] ?? 0); ?>%</p>
        </div>

        
        <?php
            $est = strtoupper($estadisticas['estado'] ?? '');
            $estColor = match(true) {
                str_contains($est, 'APROBADO')  => ['bg' => '#dcfce7', 'bd' => '#86efac', 'tx' => '#166534'],
                str_contains($est, 'RIESGO')    => ['bg' => '#fef3c7', 'bd' => '#fcd34d', 'tx' => '#92400e'],
                default                          => ['bg' => '#fee2e2', 'bd' => '#fca5a5', 'tx' => '#991b1b'],
            };
        ?>
        <div style="background: <?php echo e($estColor['bg']); ?>; border: 1px solid <?php echo e($estColor['bd']); ?>; border-radius: 0.75rem; padding: 1.25rem; text-align: center;">
            <p style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: <?php echo e($estColor['tx']); ?>; font-weight: 600; margin: 0 0 0.5rem;">Estado General</p>
            <p style="font-size: 1rem; font-weight: 700; margin: 0; color: <?php echo e($estColor['tx']); ?>;"><?php echo e($estadisticas['estado'] ?? '-'); ?></p>
        </div>

        
        <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 0.75rem; padding: 1.25rem; text-align: center;">
            <p style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: #16a34a; font-weight: 600; margin: 0 0 0.5rem;">Presentes</p>
            <p style="font-size: 2rem; font-weight: 800; margin: 0; color: #15803d;"><?php echo e($estadisticas['total_presentes'] ?? 0); ?></p>
        </div>
        <div style="background: #fff1f2; border: 1px solid #fecdd3; border-radius: 0.75rem; padding: 1.25rem; text-align: center;">
            <p style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: #e11d48; font-weight: 600; margin: 0 0 0.5rem;">Ausentes</p>
            <p style="font-size: 2rem; font-weight: 800; margin: 0; color: #be123c;"><?php echo e($estadisticas['total_ausentes'] ?? 0); ?></p>
        </div>
    </div>

    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 0.5rem; padding: 0.75rem 1rem; margin-bottom: 2rem; font-size: 0.85rem; color: #64748b;">
        Umbral de aprobación: <strong><?php echo e($estadisticas['umbral_aprobado'] ?? '-'); ?>%</strong> &nbsp;|&nbsp;
        Umbral de riesgo: <strong><?php echo e($estadisticas['umbral_riesgo'] ?? '-'); ?>%</strong> &nbsp;|&nbsp;
        Total registros: <strong><?php echo e($estadisticas['total_registros'] ?? 0); ?></strong>
    </div>
    <?php endif; ?>

    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 2rem; align-items: start;">
        <div>
            <h3 style="font-size: 1.125rem; font-weight: 600; margin: 0 0 1rem; color: var(--text-dark);">Registros de Asistencia</h3>
            <?php
                $tableRows = collect($registros)->map(fn($r) => [
                    'persona_id'   => $r['persona_id'] ?? '-',
                    'curso_id'     => $r['curso_id']   ?? '-',
                    'fecha'        => $r['fecha']       ?? '-',
                    'presente'     => $r['presente']    ?? false,
                    'justificacion'=> $r['justificacion'] ?? '-',
                ])->toArray();
            ?>
            <?php if (isset($component)) { $__componentOriginalc8463834ba515134d5c98b88e1a9dc03 = $component; } ?>
<?php if (isset($attributes)) { $__attributesOriginalc8463834ba515134d5c98b88e1a9dc03 = $attributes; } ?>
<?php $component = Illuminate\View\AnonymousComponent::resolve(['view' => 'components.data-table','data' => ['columns' => ['persona_id' => 'Persona', 'curso_id' => 'Curso', 'fecha' => 'Fecha', 'presente' => 'Presente', 'justificacion' => 'Justificación'],'rows' => $tableRows,'emptyMessage' => 'No hay registros de asistencia']] + (isset($attributes) && $attributes instanceof Illuminate\View\ComponentAttributeBag ? $attributes->all() : [])); ?>
<?php $component->withName('data-table'); ?>
<?php if ($component->shouldRender()): ?>
<?php $__env->startComponent($component->resolveView(), $component->data()); ?>
<?php if (isset($attributes) && $attributes instanceof Illuminate\View\ComponentAttributeBag): ?>
<?php $attributes = $attributes->except(\Illuminate\View\AnonymousComponent::ignoredParameterNames()); ?>
<?php endif; ?>
<?php $component->withAttributes(['columns' => \Illuminate\View\Compilers\BladeCompiler::sanitizeComponentAttribute(['persona_id' => 'Persona', 'curso_id' => 'Curso', 'fecha' => 'Fecha', 'presente' => 'Presente', 'justificacion' => 'Justificación']),'rows' => \Illuminate\View\Compilers\BladeCompiler::sanitizeComponentAttribute($tableRows),'emptyMessage' => 'No hay registros de asistencia']); ?>
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

            <?php if(!empty($resumen)): ?>
                <h3 style="font-size: 1.125rem; font-weight: 600; margin: 2rem 0 1rem; color: var(--text-dark);">Resumen por Persona</h3>
                <?php if (isset($component)) { $__componentOriginalc8463834ba515134d5c98b88e1a9dc03 = $component; } ?>
<?php if (isset($attributes)) { $__attributesOriginalc8463834ba515134d5c98b88e1a9dc03 = $attributes; } ?>
<?php $component = Illuminate\View\AnonymousComponent::resolve(['view' => 'components.data-table','data' => ['columns' => ['persona_id' => 'Persona', 'total' => 'Total', 'presentes' => 'Presentes', 'porcentaje' => 'Asistencia %', 'estado' => 'Estado'],'rows' => $resumen,'emptyMessage' => 'Sin resumen disponible']] + (isset($attributes) && $attributes instanceof Illuminate\View\ComponentAttributeBag ? $attributes->all() : [])); ?>
<?php $component->withName('data-table'); ?>
<?php if ($component->shouldRender()): ?>
<?php $__env->startComponent($component->resolveView(), $component->data()); ?>
<?php if (isset($attributes) && $attributes instanceof Illuminate\View\ComponentAttributeBag): ?>
<?php $attributes = $attributes->except(\Illuminate\View\AnonymousComponent::ignoredParameterNames()); ?>
<?php endif; ?>
<?php $component->withAttributes(['columns' => \Illuminate\View\Compilers\BladeCompiler::sanitizeComponentAttribute(['persona_id' => 'Persona', 'total' => 'Total', 'presentes' => 'Presentes', 'porcentaje' => 'Asistencia %', 'estado' => 'Estado']),'rows' => \Illuminate\View\Compilers\BladeCompiler::sanitizeComponentAttribute($resumen),'emptyMessage' => 'Sin resumen disponible']); ?>
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
            <?php endif; ?>
        </div>

        <div>
            <h3 style="font-size: 1.125rem; font-weight: 600; margin: 0 0 1rem; color: var(--text-dark);">Registrar Asistencia</h3>
            <?php if (isset($component)) { $__componentOriginalf4359a7875ba093ade2251f11a0d50c5 = $component; } ?>
<?php if (isset($attributes)) { $__attributesOriginalf4359a7875ba093ade2251f11a0d50c5 = $attributes; } ?>
<?php $component = Illuminate\View\AnonymousComponent::resolve(['view' => 'components.entity-form','data' => ['fields' => [
                    ['name' => 'persona_id',   'type' => 'select',   'label' => 'Estudiante',    'required' => true, 'options' => $personas],
                    ['name' => 'curso_id',     'type' => 'select',   'label' => 'Curso',          'required' => true, 'options' => $cursos],
                    ['name' => 'fecha',        'type' => 'date',     'label' => 'Fecha',          'required' => true],
                    ['name' => 'presente',     'type' => 'checkbox', 'label' => 'Presente'],
                    ['name' => 'justificacion','type' => 'text',     'label' => 'Justificación']
                ],'action' => '/attendance','submitLabel' => 'Guardar Asistencia']] + (isset($attributes) && $attributes instanceof Illuminate\View\ComponentAttributeBag ? $attributes->all() : [])); ?>
<?php $component->withName('entity-form'); ?>
<?php if ($component->shouldRender()): ?>
<?php $__env->startComponent($component->resolveView(), $component->data()); ?>
<?php if (isset($attributes) && $attributes instanceof Illuminate\View\ComponentAttributeBag): ?>
<?php $attributes = $attributes->except(\Illuminate\View\AnonymousComponent::ignoredParameterNames()); ?>
<?php endif; ?>
<?php $component->withAttributes(['fields' => \Illuminate\View\Compilers\BladeCompiler::sanitizeComponentAttribute([
                    ['name' => 'persona_id',   'type' => 'select',   'label' => 'Estudiante',    'required' => true, 'options' => $personas],
                    ['name' => 'curso_id',     'type' => 'select',   'label' => 'Curso',          'required' => true, 'options' => $cursos],
                    ['name' => 'fecha',        'type' => 'date',     'label' => 'Fecha',          'required' => true],
                    ['name' => 'presente',     'type' => 'checkbox', 'label' => 'Presente'],
                    ['name' => 'justificacion','type' => 'text',     'label' => 'Justificación']
                ]),'action' => '/attendance','submitLabel' => 'Guardar Asistencia']); ?>
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
<?php /**PATH C:\laragon\www\academic-spl\core_assets\frontend\laravel-shell\app\Modules/AttendanceModule/resources/views/index.blade.php ENDPATH**/ ?>