@echo off
REM ============================================================================
REM build_external.bat - Windows equivalent of build_external.sh
REM
REM Downloads (with cache) and builds the 3rd-party libraries that CMS needs:
REM   - OpenSSL  (perl Configure + nmake)
REM   - libevent (nmake -f Makefile.nmake, links against OpenSSL)
REM
REM jsoncpp is NOT handled here: its source ships in external\jsoncpp\src and is
REM compiled by the jsoncpp project inside cmserver.sln (same role as the jsoncpp
REM step of build_external.sh).
REM
REM Usage: build_external.bat [Win32|x64]   (default: Win32)
REM
REM Environment overrides:
REM   OPENSSL_VER / OPENSSL_URL     source version / download URL
REM   LIBEVENT_VER / LIBEVENT_URL   source version / download URL
REM   PERL                          full path to a native Windows perl.exe
REM   FORCE_EXTERNAL=1              rebuild even if the libraries already exist
REM ============================================================================
setlocal ENABLEDELAYEDEXPANSION

set "PERL_BADLANG=0"
set "LC_ALL=C"
set "LANG=C"
set "LC_CTYPE=C"

set PERL=D:\work_util\strawberry-perl-5.42.2.1-64bit-portable\perl\bin\perl.exe

set "SERVER_DIR=%~dp0"
if "%SERVER_DIR:~-1%" == "\" set "SERVER_DIR=%SERVER_DIR:~0,-1%"

set "platform=%~1"
if "%platform%" == "" set "platform=Win32"

REM ---- per-platform tokens -------------------------------------------------
if /I "%platform%" == "x64" (
    set "vc_arch=x64"
    set "ossl_target=VC-WIN64A"
    set "ossl_do=ms\do_win64a"
    set "ossl_out=win_64"
    set "evt_libdir=lib64"
) else (
    set "vc_arch=x86"
    set "ossl_target=VC-WIN32"
    set "ossl_do=ms\do_ms"
    set "ossl_out=win_32"
    set "evt_libdir=lib"
)

REM ---- versions / URLs (overridable) ---------------------------------------
if "%OPENSSL_VER%"  == "" set "OPENSSL_VER=1.1.1w"
if "%LIBEVENT_VER%" == "" set "LIBEVENT_VER=2.1.13-stable"
if "%OPENSSL_URL%"  == "" set "OPENSSL_URL=https://github.com/CUBRID/3rdparty/raw/develop/openssl/openssl-1.1.1w.tar.gz"
if "%LIBEVENT_URL%" == "" set "LIBEVENT_URL=https://github.com/libevent/libevent/releases/download/release-2.1.13-stable/libevent-2.1.13-stable.tar.gz"

set "EXT_DIR=%SERVER_DIR%\win\external"
set "DL_DIR=%EXT_DIR%\download"
set "OSSL_INSTALL=%EXT_DIR%\openssl\%ossl_out%"

echo ============================================================
echo  build_external : platform=%platform% (%vc_arch%)
echo    OpenSSL  %OPENSSL_VER%
echo    libevent %LIBEVENT_VER%
echo ============================================================

if not exist "%DL_DIR%" mkdir "%DL_DIR%"

REM ==========================================================================
REM  Toolchain checks
REM ==========================================================================
call :SETUP_VS
if errorlevel 1 exit /b 1

call :CHECK_PERL
if errorlevel 1 exit /b 1

call :FIND_TAR
if errorlevel 1 exit /b 1

REM ==========================================================================
REM  OpenSSL
REM ==========================================================================
if "%FORCE_EXTERNAL%" == "1" goto BUILD_OPENSSL
if exist "%OSSL_INSTALL%\lib\libcrypto.lib" if exist "%OSSL_INSTALL%\lib\libssl.lib" (
    echo [openssl ] already built at %OSSL_INSTALL%\lib - skipping ^(set FORCE_EXTERNAL=1 to rebuild^)
    goto AFTER_OPENSSL
)
:BUILD_OPENSSL
call :DOWNLOAD "%OPENSSL_URL%" "%DL_DIR%\openssl-%OPENSSL_VER%.tar.gz"
if errorlevel 1 exit /b 1
call :BUILD_OPENSSL_FN
if errorlevel 1 exit /b 1
:AFTER_OPENSSL

REM ==========================================================================
REM  libevent
REM ==========================================================================
if "%FORCE_EXTERNAL%" == "1" goto BUILD_LIBEVENT
if exist "%EXT_DIR%\libevent\%evt_libdir%\libevent.lib" if exist "%EXT_DIR%\libevent\%evt_libdir%\libevent_openssl.lib" (
    echo [libevent] already built at %EXT_DIR%\libevent\%evt_libdir% - skipping ^(set FORCE_EXTERNAL=1 to rebuild^)
    goto AFTER_LIBEVENT
)
:BUILD_LIBEVENT
call :DOWNLOAD "%LIBEVENT_URL%" "%DL_DIR%\libevent-%LIBEVENT_VER%.tar.gz"
if errorlevel 1 exit /b 1
call :BUILD_LIBEVENT_FN
if errorlevel 1 exit /b 1
:AFTER_LIBEVENT

echo.
echo [external] all 3rd-party libraries are ready for %platform%.
exit /b 0


REM ==========================================================================
REM  Subroutines
REM ==========================================================================

:SETUP_VS
REM Locate Visual Studio 2017 and import its build environment (cl / nmake / lib).
set "VSWHERE=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"
if not exist "%VSWHERE%" (
    echo [error] vswhere.exe not found. Visual Studio 2017 is required.
    exit /b 1
)
set "VSINSTALL="
set "_vstmp=%TEMP%\_cms_vsinstall.txt"
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
echo [vs      ] using "%VSINSTALL%" ^(%vc_arch%^)
call "%VCVARSALL%" %vc_arch%
if errorlevel 1 (
    echo [error] failed to initialize the Visual Studio 2017 environment.
    exit /b 1
)
exit /b 0

:CHECK_PERL
REM OpenSSL's Windows Configure/do_* scripts need a NATIVE Windows perl.
if not "%PERL%" == "" (
    if not exist "%PERL%" (
        echo [error] PERL is set to "%PERL%" but that file does not exist.
        exit /b 1
    )
    echo [perl    ] using PERL=%PERL%
    goto :CHECK_PERL_OK
)
set "PERL="
for /f "usebackq tokens=*" %%i in (`where perl 2^>nul`) do if "%PERL%"=="" set "PERL=%%i"
if "%PERL%" == "" (
    echo [error] perl was not found on PATH.
    echo         OpenSSL cannot be configured without perl.
    echo         Install a native Windows perl ^(Strawberry Perl: https://strawberryperl.com/^)
    echo         or set PERL to its perl.exe, then re-run.
    exit /b 1
)
echo %PERL% | findstr /I "\\Git\\ \\usr\\bin" >nul
if not errorlevel 1 (
    echo [warn    ] perl found at "%PERL%" looks like Git/MSYS perl.
    echo            OpenSSL's Windows build often FAILS with MSYS perl.
    echo            If the OpenSSL step fails, install Strawberry Perl and set PERL,
    echo            e.g.  set PERL=C:\Strawberry\perl\bin\perl.exe
)
:CHECK_PERL_OK
exit /b 0

:DOWNLOAD
REM %1 = url   %2 = target file  (reuse if it already exists)
set "_url=%~1"
set "_dst=%~2"
if exist "%_dst%" (
    echo [download] reuse cached "%_dst%"
    exit /b 0
)
echo [download] %_url%
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "[Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12; try { Invoke-WebRequest -Uri '%_url%' -OutFile '%_dst%' -UseBasicParsing } catch { Write-Error $_; exit 1 }"
if errorlevel 1 (
    echo [error] download failed: %_url%
    if exist "%_dst%" del /q "%_dst%"
    exit /b 1
)
exit /b 0

:BUILD_OPENSSL_FN
set "SRC=%DL_DIR%\openssl-%OPENSSL_VER%"
echo [openssl ] extracting ...
if exist "%SRC%" rmdir /s /q "%SRC%"
call :EXTRACT "%DL_DIR%\openssl-%OPENSSL_VER%.tar.gz" "%DL_DIR%"
if errorlevel 1 ( echo [error] failed to extract OpenSSL & exit /b 1 )
pushd "%SRC%"
echo [openssl ] perl Configure %ossl_target% (no-shared, no-asm)
REM OpenSSL 1.1.x build system: Configure generates a single nmake "makefile"
REM (no more ms\do_* / ms\nt.mak) and produces libcrypto.lib / libssl.lib.
"%PERL%" Configure %ossl_target% no-shared no-asm --prefix="%OSSL_INSTALL%" --openssldir="%OSSL_INSTALL%\ssl"
if errorlevel 1 ( echo [error] OpenSSL Configure failed & popd & exit /b 1 )
REM Build generated headers (opensslconf.h ...) then the libraries WITHOUT the
REM "depend" phase. The default "build_libs" runs "nmake depend && nmake
REM _build_libs"; that depend step regenerates dependency (.d) files and fails
REM under this toolchain. build_generated + build_libs_nodep skips it and still
REM produces libcrypto.lib / libssl.lib (apps/tests are not built).
echo [openssl ] nmake build_generated build_libs_nodep
nmake build_generated build_libs_nodep
if errorlevel 1 ( echo [error] OpenSSL nmake failed & popd & exit /b 1 )
REM Install the freshly built headers + static libs so both match the version
REM we just compiled (opensslconf.h is generated into include\openssl).
if not exist "%OSSL_INSTALL%\lib" mkdir "%OSSL_INSTALL%\lib"
if not exist "%OSSL_INSTALL%\include\openssl" mkdir "%OSSL_INSTALL%\include\openssl"
copy /Y libcrypto.lib "%OSSL_INSTALL%\lib\" >nul
if errorlevel 1 ( echo [error] libcrypto.lib not produced & popd & exit /b 1 )
copy /Y libssl.lib "%OSSL_INSTALL%\lib\" >nul
if errorlevel 1 ( echo [error] libssl.lib not produced & popd & exit /b 1 )
xcopy /Y "include\openssl\*.h" "%OSSL_INSTALL%\include\openssl\" >nul
if errorlevel 1 ( echo [error] OpenSSL headers not produced ^(include\openssl^) & popd & exit /b 1 )
popd
echo [openssl ] done -> %OSSL_INSTALL% ^(include + lib^)
exit /b 0

:BUILD_LIBEVENT_FN
set "SRC=%DL_DIR%\libevent-%LIBEVENT_VER%"
echo [libevent] extracting ...
if exist "%SRC%" rmdir /s /q "%SRC%"
call :EXTRACT "%DL_DIR%\libevent-%LIBEVENT_VER%.tar.gz" "%DL_DIR%"
if errorlevel 1 ( echo [error] failed to extract libevent & exit /b 1 )
pushd "%SRC%"
REM libevent 2.1.x uses UINT32_MAX (minheap-internal.h) but its Makefile.nmake
REM does not pull in <stdint.h>. Force-include it via the CL env var (read by
REM cl.exe) so every compile sees the C99 limit macros. Harmless (header is
REM guarded); avoids patching the makefile.
set "CL=/FIstdint.h"
REM Build only the static libs (the "tests" target builds regress.exe, which
REM needs if_nametoindex from iphlpapi.lib and is not needed here).
echo [libevent] nmake -f Makefile.nmake static_libs OPENSSL_DIR=%OSSL_INSTALL%
nmake OPENSSL_DIR="%OSSL_INSTALL%" -f Makefile.nmake static_libs
set "_lv_rc=!errorlevel!"
set "CL="
if not "!_lv_rc!"=="0" ( echo [error] libevent nmake failed & popd & exit /b 1 )
if not exist "%EXT_DIR%\libevent\%evt_libdir%" mkdir "%EXT_DIR%\libevent\%evt_libdir%"
copy /Y libevent*.lib "%EXT_DIR%\libevent\%evt_libdir%\" >nul
if errorlevel 1 ( echo [error] libevent*.lib not produced & popd & exit /b 1 )
REM Install libevent public headers (+ the nmake-generated event-config.h) so
REM the headers match the version we just compiled.
if not exist "%EXT_DIR%\libevent\include\event2" mkdir "%EXT_DIR%\libevent\include\event2"
xcopy /E /Y /I "include\*" "%EXT_DIR%\libevent\include\" >nul
if exist "WIN32-Code\nmake\event2\event-config.h" xcopy /Y "WIN32-Code\nmake\event2\event-config.h" "%EXT_DIR%\libevent\include\event2\" >nul
if exist "WIN32-Code\event2\event-config.h"       xcopy /Y "WIN32-Code\event2\event-config.h"       "%EXT_DIR%\libevent\include\event2\" >nul
popd
echo [libevent] done -> %EXT_DIR%\libevent ^(include + %evt_libdir%^)
exit /b 0

:FIND_TAR
REM The OpenSSL source ships symlinked headers that the Windows system tar
REM (bsdtar) cannot create ("Invalid argument"). GNU tar (bundled with Git for
REM Windows) materializes them as real files, so prefer it.
set "TAR="
if defined GNU_TAR if exist "%GNU_TAR%" set "TAR=%GNU_TAR%"
for %%p in (
    "%ProgramFiles%\Git\usr\bin\tar.exe"
    "%ProgramFiles(x86)%\Git\usr\bin\tar.exe"
    "%LOCALAPPDATA%\Programs\Git\usr\bin\tar.exe"
) do if not defined TAR if exist "%%~p" set "TAR=%%~p"
if not defined TAR (
    for /f "usebackq delims=" %%g in (`where git 2^>nul`) do (
        if not defined TAR for %%h in ("%%~dpg..") do if exist "%%~fh\usr\bin\tar.exe" set "TAR=%%~fh\usr\bin\tar.exe"
        if not defined TAR for %%h in ("%%~dpg..\..") do if exist "%%~fh\usr\bin\tar.exe" set "TAR=%%~fh\usr\bin\tar.exe"
    )
)
if not defined TAR (
    echo [error] GNU tar was not found.
    echo         The OpenSSL source contains symbolic-link headers that the
    echo         Windows system tar ^(bsdtar^) cannot extract.
    echo         Install Git for Windows ^(provides usr\bin\tar.exe^)
    echo         or set GNU_TAR to a GNU tar.exe, then re-run.
    exit /b 1
)
echo [tar     ] using "%TAR%"
exit /b 0

:EXTRACT
REM %1 = tarball   %2 = destination dir
REM GNU/MSYS tar needs forward-slash paths and --force-local for "D:\..." paths.
set "_tb=%~1"
set "_dd=%~2"
set "_tb=%_tb:\=/%"
set "_dd=%_dd:\=/%"
"%TAR%" --force-local -xf "%_tb%" -C "%_dd%"
exit /b %errorlevel%
