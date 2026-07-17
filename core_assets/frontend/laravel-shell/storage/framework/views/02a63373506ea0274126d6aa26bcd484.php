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
    <h1>Auditoría del Sistema</h1>
    <p>Historial de acciones registradas.</p>

    <div class="mt-4">
        <h3>Registros Recientes</h3>
        <?php if(empty($registros)): ?>
            <p>No hay registros de auditoría.</p>
        <?php else: ?>
            <table class="table-auto w-full mt-4 border-collapse border border-gray-200">
                <thead>
                    <tr class="bg-gray-100">
                        <th class="border px-4 py-2">ID</th>
                        <th class="border px-4 py-2">Usuario ID</th>
                        <th class="border px-4 py-2">Acción</th>
                        <th class="border px-4 py-2">Entidad</th>
                        <th class="border px-4 py-2">Entidad ID</th>
                        <th class="border px-4 py-2">Fecha/Hora</th>
                    </tr>
                </thead>
                <tbody>
                    <?php $__currentLoopData = $registros; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $log): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
                        <tr>
                            <td class="border px-4 py-2"><?php echo e($log['id'] ?? ''); ?></td>
                            <td class="border px-4 py-2"><?php echo e($log['usuario_id'] ?? ''); ?></td>
                            <td class="border px-4 py-2"><?php echo e($log['accion'] ?? ''); ?></td>
                            <td class="border px-4 py-2"><?php echo e($log['entidad'] ?? ''); ?></td>
                            <td class="border px-4 py-2"><?php echo e($log['entidad_id'] ?? ''); ?></td>
                            <td class="border px-4 py-2"><?php echo e($log['fecha_hora'] ?? ''); ?></td>
                        </tr>
                    <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>
                </tbody>
            </table>
        <?php endif; ?>
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
<?php /**PATH D:\Octavo\FABRICA\ProyectoFinal\academic-spl\core_assets\frontend\laravel-shell\app\Modules/AuditingModule/resources/views/index.blade.php ENDPATH**/ ?>