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
    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 2rem; align-items: start;">
        <div>
            <h2 style="font-size: 1.5rem; font-weight: 700; margin-top: 0; margin-bottom: 1rem; color: var(--text-dark);">
                Listado de Personas
            </h2>
            <?php if (isset($component)) { $__componentOriginalc8463834ba515134d5c98b88e1a9dc03 = $component; } ?>
<?php if (isset($attributes)) { $__attributesOriginalc8463834ba515134d5c98b88e1a9dc03 = $attributes; } ?>
<?php $component = Illuminate\View\AnonymousComponent::resolve(['view' => 'components.data-table','data' => ['columns' => ['id' => 'ID', 'nombres' => 'Nombres', 'apellidos' => 'Apellidos', 'documento_identidad' => 'Cédula / Documento'],'rows' => $personas,'emptyMessage' => 'No hay personas registradas en el sistema']] + (isset($attributes) && $attributes instanceof Illuminate\View\ComponentAttributeBag ? $attributes->all() : [])); ?>
<?php $component->withName('data-table'); ?>
<?php if ($component->shouldRender()): ?>
<?php $__env->startComponent($component->resolveView(), $component->data()); ?>
<?php if (isset($attributes) && $attributes instanceof Illuminate\View\ComponentAttributeBag): ?>
<?php $attributes = $attributes->except(\Illuminate\View\AnonymousComponent::ignoredParameterNames()); ?>
<?php endif; ?>
<?php $component->withAttributes(['columns' => \Illuminate\View\Compilers\BladeCompiler::sanitizeComponentAttribute(['id' => 'ID', 'nombres' => 'Nombres', 'apellidos' => 'Apellidos', 'documento_identidad' => 'Cédula / Documento']),'rows' => \Illuminate\View\Compilers\BladeCompiler::sanitizeComponentAttribute($personas),'emptyMessage' => 'No hay personas registradas en el sistema']); ?>
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
            <h2 style="font-size: 1.25rem; font-weight: 700; margin-top: 0; margin-bottom: 1rem; color: var(--text-dark);">
                Nueva Persona
            </h2>
            <?php if (isset($component)) { $__componentOriginalf4359a7875ba093ade2251f11a0d50c5 = $component; } ?>
<?php if (isset($attributes)) { $__attributesOriginalf4359a7875ba093ade2251f11a0d50c5 = $attributes; } ?>
<?php $component = Illuminate\View\AnonymousComponent::resolve(['view' => 'components.entity-form','data' => ['fields' => [
                    ['name' => 'nombres', 'type' => 'text', 'label' => 'Nombres', 'required' => true, 'placeholder' => 'Ej. Juan Carlos'],
                    ['name' => 'apellidos', 'type' => 'text', 'label' => 'Apellidos', 'required' => true, 'placeholder' => 'Ej. Pérez Gómez'],
                    ['name' => 'documento_identidad', 'type' => 'text', 'label' => 'Cédula / Identificación', 'required' => true, 'placeholder' => 'Ej. 1712345678']
                ],'action' => '/personas','submitLabel' => 'Registrar Persona']] + (isset($attributes) && $attributes instanceof Illuminate\View\ComponentAttributeBag ? $attributes->all() : [])); ?>
<?php $component->withName('entity-form'); ?>
<?php if ($component->shouldRender()): ?>
<?php $__env->startComponent($component->resolveView(), $component->data()); ?>
<?php if (isset($attributes) && $attributes instanceof Illuminate\View\ComponentAttributeBag): ?>
<?php $attributes = $attributes->except(\Illuminate\View\AnonymousComponent::ignoredParameterNames()); ?>
<?php endif; ?>
<?php $component->withAttributes(['fields' => \Illuminate\View\Compilers\BladeCompiler::sanitizeComponentAttribute([
                    ['name' => 'nombres', 'type' => 'text', 'label' => 'Nombres', 'required' => true, 'placeholder' => 'Ej. Juan Carlos'],
                    ['name' => 'apellidos', 'type' => 'text', 'label' => 'Apellidos', 'required' => true, 'placeholder' => 'Ej. Pérez Gómez'],
                    ['name' => 'documento_identidad', 'type' => 'text', 'label' => 'Cédula / Identificación', 'required' => true, 'placeholder' => 'Ej. 1712345678']
                ]),'action' => '/personas','submitLabel' => 'Registrar Persona']); ?>
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
<?php /**PATH C:\laragon\www\academic-spl\core_assets\frontend\laravel-shell\app\Modules/PersonasModule/resources/views/index.blade.php ENDPATH**/ ?>