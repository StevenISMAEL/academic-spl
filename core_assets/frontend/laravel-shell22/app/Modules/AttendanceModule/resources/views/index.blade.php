{{-- app/Modules/AttendanceModule/resources/views/index.blade.php --}}
<x-layout>
    <h1>Asistencia</h1>
    <table>
        <thead>
            <tr><th>Persona</th><th>Curso</th><th>Presente</th></tr>
        </thead>
        <tbody>
            @foreach ($registros as $registro)
                <tr>
                    <td>{{ $registro['persona'] }}</td>
                    <td>{{ $registro['curso'] }}</td>
                    <td>{{ $registro['presente'] ? 'Sí' : 'No' }}</td>
                </tr>
            @endforeach
        </tbody>
    </table>
</x-layout>
