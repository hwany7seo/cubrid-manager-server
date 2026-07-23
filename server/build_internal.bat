@echo off

if "%1" == "" goto PRINT_USAGE

set cubrid_dir=%CUBRID%
set platform=x64
set mode=release

REM default output dir: <this script's folder>\build_win
set script_dir=%~dp0
if "%script_dir:~-1%" == "\" set script_dir=%script_dir:~0,-1%
set prefix=

:LOOP_BEGIN

if "%1" == "" goto LOOP_END

if "%1" == "--help" goto PRINT_USAGE
if "%1" == "--prefix" set prefix=%2& shift & shift & goto LOOP_BEGIN
if "%1" == "--with-cubrid-dir" set cubrid_dir=%2& shift & shift & goto LOOP_BEGIN
if "%1" == "--with-cubrid-libdir" set cubrid_libdir=%2& shift & shift & goto LOOP_BEGIN
if "%1" == "--with-cubrid-includedir" set cubrid_includedir=%2& shift & shift & goto LOOP_BEGIN
if "%1" == "--enable-32bit" set platform=x86& shift & goto LOOP_BEGIN
if "%1" == "--enable-debug" set mode=debug& shift & goto LOOP_BEGIN

shift
:LOOP_END

if "%cubrid_libdir%" == "" (
	set cubrid_libdir=%cubrid_dir%\lib
)

if "%cubrid_includedir%" == "" (
	set cubrid_includedir=%cubrid_dir%\include
)

if "%cubrid_libdir%" == "\lib" (
	echo "Please specify --with-cubrid-libdir option"
	exit /B 1
)

if "%cubrid_includedir%" == "\include" (
	echo "Please specify --with-cubrid-includedir option"
	exit /B 1
)

REM --prefix is optional: default to <script dir>\output-win
if "%prefix%" == "" (
	set prefix=%script_dir%\output-win
	echo --prefix not specified, using default %script_dir%\output-win
)

REM MSBuild solution configuration name (proper case)
if "%mode%" == "debug" (
	set config=Debug
) else (
	set config=Release
)

echo CUBRID include path is %cubrid_includedir%
echo CUBRID lib path is %cubrid_libdir%
echo OUTPUT path is %prefix%

echo Platform type is "%platform%"
echo Debug mode is "%mode%"

if not exist %prefix% (
	mkdir %prefix%
)

REM build 3rd-party libraries (openssl, libevent) the same way build_external.sh does
call build_external.bat %platform%
set exitcode=!errorlevel!
if not "!exitcode!" == "0" (
	echo build external libraries failed
	exit /b !exitcode!
)

call build_server.bat
set exitcode=!errorlevel!

if "!exitcode!" == "0" (
	echo build successful
) else (
	echo build failed
	exit /b !exitcode!
)

set platform_token=%platform%

if "%mode%" == "debug" set is_debug=true

set target_server=pack_server

exit /b

:PRINT_USAGE
@echo Usage: build [OPTION]
@echo Build whole CUBRID Manager project
@echo.
@echo   --prefix=DIR                  build result output directory (default : output-win)
@echo                                 default to build.bat's folder\build_win
@echo   --with-cubrid-dir=DIR         directory have two sub directory (optional)
@echo                                 'include', 'lib'. default to %%CUBRID%%
@echo   --with-cubrid-libdir=DIR      directory have cubrid lib files (optional)
@echo                                 default to with_cubrid_dir\lib
@echo   --with-cubrid-includedir=DIR  directory have cubrid include files (optional)
@echo                                 default to with_cubrid_dir\include
@echo   --enable-32bit                build 32bit applications (default : 64bit)
@echo   --enable-debug                build debug version applications
@echo.
@echo   --help                        display this help and exit
@echo.
@echo   Examples:
@echo     build
@echo     build --enable-32bit --with-cubrid-dir=%%CUBRID%%
@echo     build --prefix=c:\out\x64 --with-cubrid-dir=%%CUBRID%%
