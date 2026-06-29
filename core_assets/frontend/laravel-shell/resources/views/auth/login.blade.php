<x-layout>
    <h1>Login</h1>

    @if ($errors->any())
        <div style="color: red; margin-bottom: 1rem;">
            <ul>
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        </div>
    @endif

    <form method="POST" action="{{ route('login') }}">
        @csrf
        <div style="margin-bottom: 1rem;">
            <label for="email" style="display: block; margin-bottom: 0.5rem;">Email</label>
            <input id="email" type="email" name="email" value="{{ old('email') }}" required autofocus style="padding: 0.5rem; width: 100%; max-width: 300px;">
        </div>
        
        <div style="margin-bottom: 1rem;">
            <label for="password" style="display: block; margin-bottom: 0.5rem;">Password</label>
            <input id="password" type="password" name="password" required style="padding: 0.5rem; width: 100%; max-width: 300px;">
        </div>
        
        <div>
            <button type="submit" style="padding: 0.5rem 1rem;">Login</button>
        </div>
    </form>
</x-layout>
