


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
    <h1>Panel — <?php echo e(\App\Core\Services\FeatureGate::productInfo()['product'] ?? 'Producto'); ?></h1>

    <?php if (\App\Core\Services\FeatureGate::isActive('attendance')): ?>
        <section>
            <h2>Asistencia</h2>
            <p>Aquí vive el módulo de control de asistencia.</p>
        </section>
    <?php endif; ?>

    <?php if (\App\Core\Services\FeatureGate::isActive('grading')): ?>
        <section>
            <h2>Calificaciones</h2>
            <p>Escala usada: <?php echo e(\App\Core\Services\FeatureGate::setting('academic_settings.evaluation_scale', 'numeric')); ?></p>
        </section>
    <?php endif; ?>

    <?php if (\App\Core\Services\FeatureGate::isActive('enrollment')): ?>
        <section>
            <h2>Matrícula</h2>
            <p>Aquí vive el módulo de inscripción por créditos.</p>
        </section>
    <?php endif; ?>

    <?php if (\App\Core\Services\FeatureGate::isActive('auditing')): ?>
        <section>
            <h2><a href="<?php echo e(route('auditing.index')); ?>" class="text-blue-600 hover:underline">Auditoría</a></h2>
            <p>Módulo de auditoría de acciones del sistema.</p>
        </section>
    <?php endif; ?>
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
<?php /**PATH D:\Octavo\FABRICA\ProyectoFinal\academic-spl\core_assets\frontend\laravel-shell\resources\views/dashboard.blade.php ENDPATH**/ ?>