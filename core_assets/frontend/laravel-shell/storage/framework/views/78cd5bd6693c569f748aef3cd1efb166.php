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
    $certs    = $data['certificados'] ?? [];
    $emitidos = $data['emitidos']     ?? 0;
    $rechazados = $data['rechazados'] ?? 0;
    $requisitos = $data['requisitos'] ?? [];
    $productName = $data['product_name'] ?? '';
    $nombre  = $data['nombre'] ?? null;   // cuando se filtra por persona
?>

<div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.5rem;flex-wrap:wrap;">
    <h2 style="font-size:1.5rem;font-weight:700;margin:0;color:var(--text-dark);">🎓 Certificados de Aprobación</h2>
    <?php if($productName): ?>
        <span style="background:#eff6ff;color:#1e40af;padding:.25rem .75rem;border-radius:9999px;font-size:.75rem;font-weight:600;"><?php echo e($productName); ?></span>
    <?php endif; ?>
</div>


<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1rem;margin-bottom:1.5rem;">
    <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:.5rem;padding:1rem;text-align:center;">
        <div style="font-size:.7rem;font-weight:600;color:#15803d;text-transform:uppercase;">Nota Mínima</div>
        <div style="font-size:1.5rem;font-weight:700;color:#166534;"><?php echo e($requisitos['nota_minima'] ?? '—'); ?></div>
    </div>
    <div style="background:#fefce8;border:1px solid #fde68a;border-radius:.5rem;padding:1rem;text-align:center;">
        <div style="font-size:.7rem;font-weight:600;color:#a16207;text-transform:uppercase;">Asistencia Mín.</div>
        <div style="font-size:1.5rem;font-weight:700;color:#92400e;"><?php echo e($requisitos['asistencia_minima_pct'] ?? '—'); ?>%</div>
    </div>
    <div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:.5rem;padding:1rem;text-align:center;">
        <div style="font-size:.7rem;font-weight:600;color:#1e40af;text-transform:uppercase;">Emitidos</div>
        <div style="font-size:1.5rem;font-weight:700;color:#1e3a8a;"><?php echo e($emitidos); ?></div>
    </div>
    <div style="background:#fef2f2;border:1px solid #fecaca;border-radius:.5rem;padding:1rem;text-align:center;">
        <div style="font-size:.7rem;font-weight:600;color:#b91c1c;text-transform:uppercase;">Rechazados</div>
        <div style="font-size:1.5rem;font-weight:700;color:#991b1b;"><?php echo e($rechazados); ?></div>
    </div>
</div>


<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:.5rem;padding:1.25rem;margin-bottom:1.5rem;">
    <h3 style="font-size:1rem;font-weight:700;margin:0 0 1rem;color:var(--text-dark);">Generar Certificado</h3>
    <form method="POST" action="" id="cert-form" style="display:flex;gap:.75rem;align-items:flex-end;flex-wrap:wrap;">
        <?php echo csrf_field(); ?>
        <div>
            <label style="display:block;font-size:.8rem;font-weight:600;color:#374151;margin-bottom:.375rem;">Estudiante</label>
            <select id="persona-select" name="persona_id"
                    style="padding:.5rem 1rem;border:1px solid #cbd5e1;border-radius:.375rem;font-size:.875rem;min-width:220px;">
                <option value="">— Seleccionar —</option>
                <?php $__currentLoopData = $personas; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $p): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
                    <option value="<?php echo e($p['id']); ?>"><?php echo e($p['nombres'] ?? ''); ?> <?php echo e($p['apellidos'] ?? ''); ?></option>
                <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>
            </select>
        </div>
        <button type="button" onclick="generarCertificado()"
                style="background:#1e3a8a;color:#fff;padding:.5rem 1.25rem;border:none;border-radius:.375rem;font-size:.875rem;font-weight:600;cursor:pointer;">
            🎓 Generar
        </button>
    </form>
</div>


<?php if(count($certs) > 0): ?>
    <h3 style="font-size:1rem;font-weight:700;margin:0 0 .75rem;color:var(--text-dark);">Historial de Certificados</h3>
    <table style="width:100%;border-collapse:collapse;font-size:.875rem;">
        <thead>
            <tr style="background:#f8fafc;border-bottom:2px solid #e2e8f0;">
                <th style="padding:.75rem;text-align:left;font-size:.7rem;text-transform:uppercase;color:#64748b;">Persona</th>
                <th style="padding:.75rem;text-align:center;color:#64748b;font-size:.7rem;text-transform:uppercase;">Nota Final</th>
                <th style="padding:.75rem;text-align:center;color:#64748b;font-size:.7rem;text-transform:uppercase;">Asistencia</th>
                <th style="padding:.75rem;text-align:left;color:#64748b;font-size:.7rem;text-transform:uppercase;">Estado</th>
                <th style="padding:.75rem;text-align:left;color:#64748b;font-size:.7rem;text-transform:uppercase;">Fecha</th>
                <th style="padding:.75rem;text-align:left;color:#64748b;font-size:.7rem;text-transform:uppercase;">Observación</th>
            </tr>
        </thead>
        <tbody>
            <?php $__currentLoopData = $certs; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $c): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); ?>
                <?php
                    $esEmitido = $c['estado'] === 'emitido';
                    $color = $esEmitido ? '#15803d' : '#b91c1c';
                    $bg    = $esEmitido ? '#dcfce7'  : '#fee2e2';
                    $icon  = $esEmitido ? '✅' : '❌';
                ?>
                <tr style="border-bottom:1px solid #f1f5f9;">
                    <td style="padding:.75rem;font-family:monospace;font-size:.8rem;"><?php echo e($c['persona_id']); ?></td>
                    <td style="padding:.75rem;text-align:center;font-weight:600;">
                        <?php echo e($c['nota_final'] !== null ? number_format($c['nota_final'], 2) : '—'); ?>

                    </td>
                    <td style="padding:.75rem;text-align:center;">
                        <?php echo e($c['asistencia_pct'] !== null ? number_format($c['asistencia_pct'], 1).'%' : '—'); ?>

                    </td>
                    <td style="padding:.75rem;">
                        <span style="background:<?php echo e($bg); ?>;color:<?php echo e($color); ?>;padding:.2rem .625rem;border-radius:9999px;font-size:.75rem;font-weight:600;">
                            <?php echo e($icon); ?> <?php echo e(strtoupper($c['estado'])); ?>

                        </span>
                    </td>
                    <td style="padding:.75rem;font-size:.8rem;color:#64748b;"><?php echo e($c['fecha_emision']); ?></td>
                    <td style="padding:.75rem;font-size:.8rem;color:#64748b;"><?php echo e($c['motivo_rechazo'] ?? '—'); ?></td>
                </tr>
            <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); ?>
        </tbody>
    </table>
<?php else: ?>
    <p style="color:#64748b;font-style:italic;">No hay certificados registrados aún. Usa el formulario para generar el primero.</p>
<?php endif; ?>

<script>
function generarCertificado() {
    const select = document.getElementById('persona-select');
    const personaId = select.value;
    if (!personaId) { alert('Selecciona un estudiante primero.'); return; }

    const form = document.getElementById('cert-form');
    form.action = '/certificates/' + personaId + '/generate';
    form.submit();
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
<?php /**PATH D:\Octavo\FABRICA\ProyectoFinal\academic-spl\core_assets\frontend\laravel-shell\app\Modules/CertificatesModule/resources/views/index.blade.php ENDPATH**/ ?>