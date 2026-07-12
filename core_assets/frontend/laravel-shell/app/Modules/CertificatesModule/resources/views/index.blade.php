<x-layout>
    <h2 style="font-size: 1.5rem; font-weight: 700; margin: 0 0 1rem; color: var(--text-dark);">Certificados</h2>
    <div style="background:#fef3c7;border:1px solid #fcd34d;border-radius:0.5rem;padding:1.25rem;color:#92400e;font-size:0.875rem;">
        <p style="margin:0;font-weight:600;">🚧 Módulo en desarrollo (Sprint 3)</p>
        <p style="margin:0.25rem 0 0;">La generación de certificados académicos estará disponible en el próximo sprint.</p>
    </div>
    @if(!empty($certificados))
        <pre style="margin-top:1.5rem;background:#f8fafc;padding:1rem;border-radius:0.5rem;font-size:0.8rem;overflow:auto;">{{ json_encode($certificados, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) }}</pre>
    @endif
</x-layout>
