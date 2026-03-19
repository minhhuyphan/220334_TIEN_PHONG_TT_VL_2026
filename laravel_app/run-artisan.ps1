# Update PATH to use XAMPP PHP first
$env:Path = "C:\xampp\php;" + [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Run artisan with arguments
C:\xampp\php\php.exe artisan @args
