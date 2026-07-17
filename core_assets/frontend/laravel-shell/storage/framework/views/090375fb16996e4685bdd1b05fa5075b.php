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
<?php
    $horarios      = $data['horarios']          ?? [];
    $horariosPorDia = $data['horarios_por_dia'] ?? [];
    $periodsPerYear = $data['periods_per_year'] ?? 2;
    $productName    = $data['product_name']     ?? '';
    $diasValidos    = $data['dias_validos']      ?? ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado'];
?>

<div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.5rem;flex-wrap:wrap;">
    <h2 style="font-size:1.5rem;font-weight:700;margin:0;color:var(--text-dark);">🗓 Horarios de Clases</h2>
    <span style="background:#eff6ff;color:#1e40af;padding:.25rem .75rem;border-radius:9999px;font-size:.75rem;font-weight:600;">
        <?php echo e($productName); ?> · <?php echo e($periodsPerYear); ?> período(s)/año
    </span>
    <span style="margin-left:auto;background:#f0fdf4;color:#15803d;padding:.25rem .75rem;border-radius:9999px;font-size:.75rem;font-weight:600;">
        <?php echo e(count($horarios)); ?> horarios registrados
    </span>
</div>


<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:.5rem;padding:1.25rem;margin-bottom:1.5rem;">
    <h3 style="font-size:1rem;font-weight:700;margin:0 0 1rem;color:var(--text-dark);">Agregar Bloque de Horario</h3>
    <form method="POST" action="<?php echo e(route('schedule.store')); ?>" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:.75rem;align-items:end;">
        <?php echo csrf_field(); ?>
        <div>
            <label style="display:block;font-size:.8rem;font-weight:600;color:#374151;margin-bottom:.375rem;">Curso *</label>
            <select name="curso_id" required style="width:100%;padding:.5rem;border:1px solid #cbd5e1;border-radius:.375rem;font-size:.875rem;box-sizing:border-box;">
                <option value="">— Seleccionar —</option>
                <?php $__currentLoopData = $cursos; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $c): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
                    <option value="<?php echo e($c['id']); ?>"><?php echo e($c['nombre']); ?></option>
                <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>
            </select>
        </div>
        <div>
            <label style="display:block;font-size:.8rem;font-weight:600;color:#374151;margin-bottom:.375rem;">Día *</label>
            <select name="dia_semana" required style="width:100%;padding:.5rem;border:1px solid #cbd5e1;border-radius:.375rem;font-size:.875rem;box-sizing:border-box;">
                <option value="">— Seleccionar —</option>
                <?php $__currentLoopData = $diasValidos; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $dia): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
                    <option value="<?php echo e($dia); ?>"><?php echo e($dia); ?></option>
                <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>
            </select>
        </div>
        <div>
            <label style="display:block;font-size:.8rem;font-weight:600;color:#374151;margin-bottom:.375rem;">Hora Inicio *</label>
            <input type="time" name="hora_inicio" required
                   style="width:100%;padding:.5rem;border:1px solid #cbd5e1;border-radius:.375rem;font-size:.875rem;box-sizing:border-box;">
        </div>
        <div>
            <label style="display:block;font-size:.8rem;font-weight:600;color:#374151;margin-bottom:.375rem;">Hora Fin *</label>
            <input type="time" name="hora_fin" required
                   style="width:100%;padding:.5rem;border:1px solid #cbd5e1;border-radius:.375rem;font-size:.875rem;box-sizing:border-box;">
        </div>
        <div>
            <label style="display:block;font-size:.8rem;font-weight:600;color:#374151;margin-bottom:.375rem;">Aula</label>
            <input type="text" name="aula" placeholder="Ej: A-101"
                   style="width:100%;padding:.5rem;border:1px solid #cbd5e1;border-radius:.375rem;font-size:.875rem;box-sizing:border-box;">
        </div>
        <div style="display:flex;align-items:flex-end;">
            <button type="submit"
                    style="width:100%;background:#1e3a8a;color:#fff;padding:.55rem 1rem;border:none;border-radius:.375rem;font-size:.875rem;font-weight:600;cursor:pointer;">
                ➕ Agregar
            </button>
        </div>
    </form>
</div>


<?php if(count($horariosPorDia) > 0): ?>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:1rem;margin-bottom:1.5rem;">
        <?php $__currentLoopData = $horariosPorDia; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $dia => $bloques): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
            <div style="background:#fff;border:1px solid #e2e8f0;border-radius:.5rem;overflow:hidden;">
                <div style="background:#1e3a8a;color:#fff;padding:.625rem 1rem;font-weight:700;font-size:.875rem;">
                    📅 <?php echo e($dia); ?>

                    <span style="float:right;background:rgba(255,255,255,.2);padding:.1rem .5rem;border-radius:9999px;font-size:.75rem;"><?php echo e(count($bloques)); ?></span>
                </div>
                <?php $__currentLoopData = $bloques; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $b): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
                    <div style="padding:.75rem 1rem;border-bottom:1px solid #f1f5f9;display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <div style="font-weight:600;font-size:.875rem;"><?php echo e($b['hora_inicio']); ?> – <?php echo e($b['hora_fin']); ?></div>
                            <div style="font-size:.8rem;color:#64748b;"><?php echo e($b['nombre_curso'] ?? $b['curso_id']); ?></div>
                            <?php if($b['aula']): ?>
                                <div style="font-size:.75rem;color:#94a3b8;">Aula: <?php echo e($b['aula']); ?></div>
                            <?php endif; ?>
                        </div>
                        <form method="POST" action="<?php echo e(route('schedule.destroy', $b['id'])); ?>" onsubmit="return confirm('¿Eliminar este horario?')">
                            <?php echo csrf_field(); ?>
                            <?php echo method_field('DELETE'); ?>
                            <button type="submit"
                                    style="background:#fee2e2;color:#b91c1c;border:none;padding:.3rem .6rem;border-radius:.375rem;font-size:.75rem;cursor:pointer;">
                                🗑
                            </button>
                        </form>
                    </div>
                <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>
            </div>
        <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>
    </div>
<?php endif; ?>


<?php if(count($horarios) > 0): ?>
    <h3 style="font-size:1rem;font-weight:700;margin:0 0 .75rem;color:var(--text-dark);">Lista Completa</h3>
    <table style="width:100%;border-collapse:collapse;font-size:.875rem;">
        <thead>
            <tr style="background:#f8fafc;border-bottom:2px solid #e2e8f0;">
                <th style="padding:.75rem;text-align:left;font-size:.7rem;text-transform:uppercase;color:#64748b;">Curso</th>
                <th style="padding:.75rem;text-align:center;color:#64748b;font-size:.7rem;text-transform:uppercase;">Día</th>
                <th style="padding:.75rem;text-align:center;color:#64748b;font-size:.7rem;text-transform:uppercase;">Inicio</th>
                <th style="padding:.75rem;text-align:center;color:#64748b;font-size:.7rem;text-transform:uppercase;">Fin</th>
                <th style="padding:.75rem;text-align:center;color:#64748b;font-size:.7rem;text-transform:uppercase;">Aula</th>
                <th style="padding:.75rem;text-align:center;color:#64748b;font-size:.7rem;text-transform:uppercase;">Acción</th>
            </tr>
        </thead>
        <tbody>
            <?php $__currentLoopData = $horarios; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $h): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
                <tr style="border-bottom:1px solid #f1f5f9;">
                    <td style="padding:.75rem;font-weight:500;"><?php echo e($h['nombre_curso'] ?? $h['curso_id']); ?></td>
                    <td style="padding:.75rem;text-align:center;">
                        <span style="background:#eff6ff;color:#1e40af;padding:.2rem .5rem;border-radius:9999px;font-size:.75rem;font-weight:600;"><?php echo e($h['dia_semana']); ?></span>
                    </td>
                    <td style="padding:.75rem;text-align:center;"><?php echo e($h['hora_inicio']); ?></td>
                    <td style="padding:.75rem;text-align:center;"><?php echo e($h['hora_fin']); ?></td>
                    <td style="padding:.75rem;text-align:center;color:#64748b;"><?php echo e($h['aula'] ?? '—'); ?></td>
                    <td style="padding:.75rem;text-align:center;">
                        <form method="POST" action="<?php echo e(route('schedule.destroy', $h['id'])); ?>" onsubmit="return confirm('¿Eliminar?')" style="display:inline;">
                            <?php echo csrf_field(); ?>
                            <?php echo method_field('DELETE'); ?>
                            <button type="submit" style="background:#fee2e2;color:#b91c1c;border:none;padding:.3rem .75rem;border-radius:.375rem;font-size:.8rem;cursor:pointer;">
                                Eliminar
                            </button>
                        </form>
                    </td>
                </tr>
            <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>
        </tbody>
    </table>
<?php else: ?>
    <p style="color:#64748b;font-style:italic;">No hay horarios registrados aún. Agrega el primer bloque usando el formulario.</p>
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
<?php /**PATH D:\Octavo\FABRICA\ProyectoFinal\academic-spl\core_assets\frontend\laravel-shell\app\Modules/ScheduleModule/resources/views/index.blade.php ENDPATH**/ ?>