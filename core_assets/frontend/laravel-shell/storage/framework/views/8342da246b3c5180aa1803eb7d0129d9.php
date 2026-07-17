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
<h2 style="font-size:1.5rem;font-weight:700;margin:0 0 1.5rem;color:var(--text-dark);">📊 Reportes Académicos</h2>


<?php
    $config = $reportes['configuracion_producto'] ?? [];
    $personas = $reportes['personas_disponibles'] ?? [];
?>

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:1rem;margin-bottom:1.5rem;">
    <div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:0.5rem;padding:1rem;text-align:center;">
        <div style="font-size:0.7rem;font-weight:600;color:#1e40af;text-transform:uppercase;letter-spacing:.05em;">Producto</div>
        <div style="font-size:1rem;font-weight:700;color:#1e3a8a;margin-top:.25rem;"><?php echo e($config['product_name'] ?? '—'); ?></div>
    </div>
    <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:0.5rem;padding:1rem;text-align:center;">
        <div style="font-size:0.7rem;font-weight:600;color:#15803d;text-transform:uppercase;letter-spacing:.05em;">Nota Mínima</div>
        <div style="font-size:1.5rem;font-weight:700;color:#166534;margin-top:.25rem;"><?php echo e($config['passing_grade'] ?? '—'); ?></div>
    </div>
    <div style="background:#fefce8;border:1px solid #fde68a;border-radius:0.5rem;padding:1rem;text-align:center;">
        <div style="font-size:0.7rem;font-weight:600;color:#a16207;text-transform:uppercase;letter-spacing:.05em;">Asistencia Mín.</div>
        <div style="font-size:1.5rem;font-weight:700;color:#92400e;margin-top:.25rem;"><?php echo e($config['attendance_min_percentage'] ?? '—'); ?>%</div>
    </div>
    <div style="background:#f5f3ff;border:1px solid #ddd6fe;border-radius:0.5rem;padding:1rem;text-align:center;">
        <div style="font-size:0.7rem;font-weight:600;color:#6d28d9;text-transform:uppercase;letter-spacing:.05em;">Escala</div>
        <div style="font-size:1rem;font-weight:700;color:#4c1d95;margin-top:.25rem;"><?php echo e(ucfirst($config['evaluation_scale'] ?? '—')); ?></div>
    </div>
</div>


<div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.5rem;flex-wrap:wrap;">
    <label style="font-weight:600;font-size:0.9rem;color:var(--text-dark);">Ver reporte de:</label>
    <select id="persona-select" onchange="verReporte(this.value)"
            style="padding:.5rem 1rem;border:1px solid #cbd5e1;border-radius:.375rem;font-size:.875rem;background:#fff;cursor:pointer;min-width:220px;">
        <option value="">— Seleccionar estudiante —</option>
        <?php $__currentLoopData = $personas; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $p): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
            <option value="<?php echo e($p['id']); ?>"><?php echo e($p['nombre']); ?></option>
        <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>
    </select>
    <a href="/reports/consolidado"
       style="background:#1e3a8a;color:#fff;padding:.5rem 1.25rem;border-radius:.375rem;font-size:.875rem;font-weight:600;text-decoration:none;">
        📋 Consolidado General
    </a>
</div>


<div id="reporte-panel"></div>


<?php if(!empty($reportes['consolidado'])): ?>
    <?php $consolidado = $reportes; ?>
    <h3 style="font-size:1.1rem;font-weight:700;margin:0 0 1rem;color:var(--text-dark);">
        Consolidado — <?php echo e($consolidado['product_name'] ?? ''); ?>

    </h3>

    
    <?php $estados = $consolidado['resumen_estados'] ?? []; ?>
    <div style="display:flex;gap:.75rem;flex-wrap:wrap;margin-bottom:1.25rem;">
        <?php $__currentLoopData = $estados; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $estado => $count): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
            <?php
                $color = match($estado) {
                    'APROBADO'       => '#15803d',
                    'REPROBADO_NOTA' => '#b91c1c',
                    'REPROBADO_FALTA'=> '#c2410c',
                    'EN_RIESGO'      => '#b45309',
                    default          => '#475569',
                };
                $bg = match($estado) {
                    'APROBADO'       => '#dcfce7',
                    'REPROBADO_NOTA' => '#fee2e2',
                    'REPROBADO_FALTA'=> '#ffedd5',
                    'EN_RIESGO'      => '#fef3c7',
                    default          => '#f1f5f9',
                };
            ?>
            <span style="background:<?php echo e($bg); ?>;color:<?php echo e($color); ?>;padding:.375rem .75rem;border-radius:9999px;font-size:.8rem;font-weight:600;">
                <?php echo e($estado); ?>: <?php echo e($count); ?>

            </span>
        <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>
    </div>

    <table style="width:100%;border-collapse:collapse;font-size:.875rem;">
        <thead>
            <tr style="background:#f8fafc;border-bottom:2px solid #e2e8f0;">
                <th style="padding:.75rem;text-align:left;font-size:.75rem;text-transform:uppercase;letter-spacing:.05em;color:#64748b;">Estudiante</th>
                <th style="padding:.75rem;text-align:center;color:#64748b;font-size:.75rem;text-transform:uppercase;">Promedio</th>
                <th style="padding:.75rem;text-align:center;color:#64748b;font-size:.75rem;text-transform:uppercase;">Asistencia</th>
                <th style="padding:.75rem;text-align:center;color:#64748b;font-size:.75rem;text-transform:uppercase;">Estado Final</th>
            </tr>
        </thead>
        <tbody>
            <?php $__currentLoopData = $consolidado['consolidado']; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $fila): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
                <?php
                    $ef = $fila['estado_final'];
                    $badgeColor = match($ef) {
                        'APROBADO'        => '#15803d',
                        'REPROBADO_NOTA'  => '#b91c1c',
                        'REPROBADO_FALTA' => '#c2410c',
                        'EN_RIESGO'       => '#b45309',
                        default           => '#475569',
                    };
                    $badgeBg = match($ef) {
                        'APROBADO'        => '#dcfce7',
                        'REPROBADO_NOTA'  => '#fee2e2',
                        'REPROBADO_FALTA' => '#ffedd5',
                        'EN_RIESGO'       => '#fef3c7',
                        default           => '#f1f5f9',
                    };
                ?>
                <tr style="border-bottom:1px solid #f1f5f9;">
                    <td style="padding:.75rem;font-weight:500;"><?php echo e($fila['nombre_completo']); ?></td>
                    <td style="padding:.75rem;text-align:center;">
                        <?php echo e($fila['promedio'] !== null ? number_format($fila['promedio'], 2) : '—'); ?>

                    </td>
                    <td style="padding:.75rem;text-align:center;">
                        <?php echo e($fila['asistencia_pct'] !== null ? number_format($fila['asistencia_pct'], 1).'%' : '—'); ?>

                    </td>
                    <td style="padding:.75rem;text-align:center;">
                        <span style="background:<?php echo e($badgeBg); ?>;color:<?php echo e($badgeColor); ?>;padding:.25rem .625rem;border-radius:9999px;font-size:.75rem;font-weight:600;">
                            <?php echo e($ef); ?>

                        </span>
                    </td>
                </tr>
            <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>
        </tbody>
    </table>
<?php endif; ?>

<script>
function verReporte(personaId) {
    if (!personaId) { document.getElementById('reporte-panel').innerHTML = ''; return; }
    window.location.href = '/reports/rendimiento/' + personaId;
}
</script>
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
<?php /**PATH D:\Octavo\FABRICA\ProyectoFinal\academic-spl\core_assets\frontend\laravel-shell\app\Modules/ReportsModule/resources/views/index.blade.php ENDPATH**/ ?>