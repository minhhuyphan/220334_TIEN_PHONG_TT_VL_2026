<!doctype html>
<html lang="en">

<head>
    @include('user.components.head')
</head>

<body class="bg-light">
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-3 px-4">
                @include('user.components.sidebar')
            </div>
            <div class="col-md-9 vh-100">
                @yield('content')
            </div>
        </div>
    </div>

    @include('user.components.script')

    @yield('scripts')
</body>

</html>