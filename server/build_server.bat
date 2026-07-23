@echo off

REM prepare Visual Studio 2017 (v141) build environment

SET VERS=win/version.h
SET COMMIT_COUNT=

REM ---- locate Visual Studio 2017 and import its environment ----------------
set "VSWHERE=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"
if not exist "%VSWHERE%" (
	echo [error] vswhere.exe not found. Visual Studio 2017 is required.
	exit /b 1
)
set "VSINSTALL="
set "_vstmp=%TEMP%\_cms_vsinstall_srv.txt"
"%VSWHERE%" -version "[15.0,16.0)" -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath > "%_vstmp%" 2>nul
if exist "%_vstmp%" set /p VSINSTALL=<"%_vstmp%"
if not defined VSINSTALL (
	"%VSWHERE%" -version "[15.0,16.0)" -products * -property installationPath > "%_vstmp%" 2>nul
	if exist "%_vstmp%" set /p VSINSTALL=<"%_vstmp%"
)
del "%_vstmp%" 2>nul
if not defined VSINSTALL (
	echo [error] Visual Studio 2017 ^(v141 C++ toolset^) was not found by vswhere.
	exit /b 1
)
set "VCVARSALL=%VSINSTALL%\VC\Auxiliary\Build\vcvarsall.bat"
if not exist "%VCVARSALL%" (
	echo [error] vcvarsall.bat not found under "%VSINSTALL%".
	exit /b 1
)

set vc_arch=x86
if /I "%platform%" == "x64" set vc_arch=x64
if "%config%" == "" set config=Release

echo Using Visual Studio 2017 at "%VSINSTALL%" ^(%vc_arch%^)
call "%VCVARSALL%" %vc_arch%
if errorlevel 1 (
	echo [error] failed to initialize the Visual Studio 2017 environment.
	exit /b 1
)

REM ---- generate version.h --------------------------------------------------
FOR /F "tokens=1 delims=." %%i IN ('type BUILD_NUMBER') do (SET MAJOR=%%i)
FOR /F "tokens=2 delims=." %%i IN ('type BUILD_NUMBER') do (SET MINOR=%%i)
FOR /F "tokens=3 delims=." %%i IN ('type BUILD_NUMBER') do (SET PATCH=%%i)
FOR /F "tokens=4 delims=." %%i IN ('type BUILD_NUMBER') do (SET SERIAL=%%i)
if not ERRORLEVEL 0 (exit /b %ERRORLEVEL%)

FOR /F "tokens=*" %%i IN ('git rev-list --count HEAD') do (SET COMMIT_COUNT=%%i)
if "%COMMIT_COUNT%" == "" (SET COMMIT_COUNT=%SERIAL%)

FOR /F "tokens=* delims=0" %%i IN ('echo %COMMIT_COUNT%') do (SET COMMIT_COUNT=%%i)
FOR /F "tokens=*" %%i IN ('printf %%04d %COMMIT_COUNT%') do (SET COMMIT_COUNT=%%i)

echo #define RELEASE_STRING %MAJOR%.%MINOR%.%PATCH% > %VERS%
echo #define MAJOR_RELEASE_STRING %MAJOR% >> %VERS%
echo #define BUILD_NUMBER %MAJOR%.%MINOR%.%PATCH%.%COMMIT_COUNT% >> %VERS%
echo #define MAJOR_VERSION %MAJOR% >> %VERS%
echo #define MINOR_VERSION %MINOR% >> %VERS%
echo #define PATCH_VERSION %PATCH% >> %VERS%
echo #define BUILD_SERIAL_NUMBER %COMMIT_COUNT% >> %VERS%
echo #define VERSION_STRING "%MAJOR%.%MINOR%.%PATCH%.%COMMIT_COUNT%" >> %VERS%

REM ---- pick the latest installed Windows 10 SDK -----------------------------
set win_sdk=
for /f "usebackq tokens=*" %%i in (`powershell -NoProfile -Command "$r=(Get-ItemProperty 'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Microsoft SDKs\Windows\v10.0' -ErrorAction SilentlyContinue).InstallationFolder; if($r){ Get-ChildItem (Join-Path $r 'Include') -Directory | Where-Object { $_.Name -like '10.*' } | Sort-Object Name | Select-Object -Last 1 -ExpandProperty Name }"`) do set win_sdk=%%i
if not "%win_sdk%" == "" (
	echo Using Windows SDK %win_sdk%
	set win_sdk_prop=/p:WindowsTargetPlatformVersion=%win_sdk%
) else (
	echo [warn] no Windows 10 SDK detected; using project default
	set win_sdk_prop=
)

echo Start build cm_server ...
cd win

set cubrid_libdir=%cubrid_libdir%
set cubrid_includedir=%cubrid_includedir%

REM Build the whole solution with MSBuild (v141). Solution dependencies make
REM jsoncpp -> cub_manager / cm_admin -> install build in the right order, and
REM the install project packages the binaries into CMServer_<config>_<platform>.
msbuild cmserver.sln /nologo /m /t:Build /p:Configuration=%config%;Platform=%platform% %win_sdk_prop%
set exitcode=%errorlevel%
cd ..
if not "%exitcode%" == "0" exit /b %exitcode%

cd win/install
cd CMServer_%mode%_%platform%

robocopy . %prefix%\ /e
if errorlevel 1 (
	set exitcode=0
	) else (
	set exitcode=%errorlevel%
	)
cd ..\..\..

