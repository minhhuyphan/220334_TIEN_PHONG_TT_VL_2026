@echo off
REM Start Laravel development server with XAMPP's PHP
C:\xampp\php\php.exe "%~dp0artisan" serve --host=127.0.0.1 --port=8000
